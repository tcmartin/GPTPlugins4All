import os
import time
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class Assistant:
    def __init__(self, config, name, instructions, model):
        self.config = config
        self.name = name
        self.instructions = instructions
        self.model = model
        self.openai_client = OpenAI()
        self.assistant, self.thread = self.create_assistant_and_thread()

    # Create an OpenAI assistant and a thread for interactions
    def create_assistant_and_thread(self):
        # Extract tools from the Alpha Vantage config
        tools = self.config.generate_tools_representation()
        desc_string = ""
        if self.config.model_description is not None and self.config.model_description != "none":
            desc_string =  " Tool information below\n---------------\n"+self.config.model_description
        # Initialize the OpenAI assistant
        if os.getenv("ASSISTANT_ID") is not None:
            assistant = self.openai_client.beta.assistants.retrieve(os.getenv("ASSISTANT_ID"))
            if os.getenv("THREAD_ID") is not None:
                thread = self.openai_client.beta.threads.retrieve(os.getenv("THREAD_ID"))
                runs = self.openai_client.beta.threads.runs.list(os.getenv("THREAD_ID"))
                if len(runs.data) > 0:
                    latest_run = runs.data[0]
                    if(latest_run.status == "in_progress" or latest_run.status == "queued" or latest_run.status == "requires_action"):
                        run = self.openai_client.beta.threads.runs.cancel(thread_id=os.getenv("THREAD_ID"), run_id = latest_run.id)
                        print('cancelled run')
            else:
                thread = self.openai_client.beta.threads.create()
                print("Thread ID: save this for persistence: "+thread.id)
        else:
            assistant = self.openai_client.beta.assistants.create(
                name="Finance Assistant",
                instructions=self.instructions+desc_string,
                model=self.model,
                tools=tools,
            )
            print("Assistant ID: save this for persistence: "+assistant.id)
            thread = self.openai_client.beta.threads.create()
            print("Thread ID: save this for persistence: "+thread.id)

        # Create a thread for the assistant
        return assistant, thread


    def get_assistant_response(self,message):
        message = self.openai_client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )
        run = self.openai_client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            #instructions="Please address the user as Jane Doe. The user has a premium account."
            )
        print("Waiting for response")
        print(run.id)
        completed = False
        while not completed:
            run_ = self.openai_client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
            if run_.status == "completed":
                break
            elif run_.status == "failed":
                print("Run failed")
                break
            elif run_.status == "cancelled":
                print("Run cancelled")
                break
            elif run_.status == "requires_action":
                print("Run requires action")
                tool_calls = run_.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []
                for tool_call in tool_calls:
                    print(tool_call)
                    if tool_call.type == "function":
                        result = self.execute_function(tool_call.function.name, tool_call.function.arguments, self.config)
                        output = {
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(result)
                        }
                        print(output)
                        tool_outputs.append(output)
                run__ = self.openai_client.beta.threads.runs.submit_tool_outputs(thread_id=self.thread.id, run_id=run.id, tool_outputs=tool_outputs)
            time.sleep(5)
        run_ = self.openai_client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
        messages = self.openai_client.beta.threads.messages.list(thread_id=self.thread.id)
        print(messages)
        print(messages.data[0].content[0].text.value)
        return messages.data[0].content[0].text.value
    def execute_function(self,function_name, arguments):
        """Execute a function and return the result."""
        #example of function_name: "alpha_vantage/query"
        #config.make_api_call_by_operation_id("genericQuery", params={"function": "TIME_SERIES_DAILY", "symbol": "BTC", "market": "USD"}
        #config.make_api_call_by_path("/query", "GET", params={"function": "TIME_SERIES_DAILY", "symbol": "BTC", "market": "USD"})
        #actual implementation of the function
        print(function_name)
        print(arguments)
        #turn arguments into dictionary
        arguments = json.loads(arguments)
        try:
            request = self.config.make_api_call_by_operation_id(function_name, params=arguments)
            print(request.json())
            return request.json()
        except Exception as e:
            print(e)
            try:
                #split the function name into path and method by - eg query-GET
                split = function_name.split("-")
                method = split[1]
                path = split[0]
                print('got here')
                print(path)
                print(method.upper())
                request = self.config.make_api_call_by_path('/'+path, method.upper(), params=arguments)
                print(request.json())
                return request.json()
            except Exception as e:
                print(e)
                #debug stack trace
                import traceback
                traceback.print_exc()
                try:
                    print('got here 2')
                    request = self.config.make_api_call_by_path(path, method.upper(), params=arguments)
                    print(request.json())
                    return request.json()
                except Exception as e:
                    print(e)
                    return "Error"
