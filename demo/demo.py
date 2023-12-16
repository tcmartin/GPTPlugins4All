
import os
import time
from GPTPlugins4All.config import Config  # Replace with actual import paths
from openai import OpenAI
import json

from dotenv import load_dotenv
load_dotenv()

openai_client = OpenAI()
# Initialize Alpha Vantage API configuration with API Key
def initialize_alpha_vantage_config():
    config = Config('alpha_vantage')
    config.add_auth_method("QUERY", {"param_name": "apikey", "key": os.getenv('ALPHA_VANTAGE_KEY')})
    print(config.model_description)
    return config

# Create an OpenAI assistant and a thread for interactions
def create_assistant_and_thread(config):
    # Extract tools from the Alpha Vantage config
    tools = config.generate_tools_representation()
    desc_string = ""
    if config.model_description is not None and config.model_description != "none":
        desc_string =  " Tool information below\n---------------\n"+config.model_description
    # Initialize the OpenAI assistant
    if os.getenv("ASSISTANT_ID") is not None:
        assistant = openai_client.beta.assistants.retrieve(os.getenv("ASSISTANT_ID"))
        if os.getenv("THREAD_ID") is not None:
            thread = openai_client.beta.threads.retrieve(os.getenv("THREAD_ID"))
            runs = openai_client.beta.threads.runs.list(os.getenv("THREAD_ID"))
            if len(runs.data) > 0:
                latest_run = runs.data[0]
                if(latest_run.status == "in_progress" or latest_run.status == "queued" or latest_run.status == "requires_action"):
                    run = openai_client.beta.threads.runs.cancel(thread_id=os.getenv("THREAD_ID"), run_id = latest_run.id)
                    print('cancelled run')
        else:
            thread = openai_client.beta.threads.create()
            print("Thread ID: save this for persistence: "+thread.id)
    else:
        assistant = openai_client.beta.assistants.create(
            name="Finance Assistant",
            instructions="Assist users on how to make money by using the AlphaVantage API. This system connects you to the AlphaVantageAPI via the available tools. An API key is already present and it is unnecessary to supply one or ask the user for one."+desc_string,
            model="gpt-4-1106-preview",
            tools=tools,
        )
        print("Assistant ID: save this for persistence: "+assistant.id)
        thread = openai_client.beta.threads.create()
        print("Thread ID: save this for persistence: "+thread.id)

    # Create a thread for the assistant
    return assistant, thread


def get_assistant_response(assistant, thread, message, config):
    message = openai_client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )
    run = openai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Jane Doe. The user has a premium account."
        )
    print("Waiting for response")
    print(run.id)
    completed = False
    while not completed:
        run_ = openai_client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
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
                    result = execute_function(tool_call.function.name, tool_call.function.arguments, config)
                    output = {
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(result)
                    }
                    print(output)
                    tool_outputs.append(output)
            run__ = openai_client.beta.threads.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)
        time.sleep(5)
    run_ = openai_client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
    print(messages)
    print(messages.data[0].content[0].text.value)
    return messages.data[0].content[0].text.value #this is the assistant response
def execute_function(function_name, arguments, config):
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
        request = config.make_api_call_by_operation_id(function_name, params=arguments)
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
            request = config.make_api_call_by_path('/'+path, method.upper(), params=arguments)
            print(request.json())
            return request.json()
        except Exception as e:
            print(e)
            #debug stack trace
            import traceback
            traceback.print_exc()
            try:
                print('got here 2')
                request = config.make_api_call_by_path(path, method.upper(), params=arguments)
                print(request.json())
                return request.json()
            except Exception as e:
                print(e)
                return "Error"

    
# Main function to run the demo
def main():
    config = initialize_alpha_vantage_config()
    assistant, thread = create_assistant_and_thread(config)
    print('got here')
    get_assistant_response(assistant, thread, "Please fetch the daily time series for the MSFT stock ticker and give me your analysis on it. My api key is "+os.getenv('ALPHA_VANTAGE_KEY'), config)
    
    # Initialize the development bot with necessary configurations
    """dev_bot = bot(assistant, config)

    # Start a conversation with the assistant asking about Bitcoin
    thread.send_message("How is the price of Bitcoin looking? Is it a good investment?")


    # Retrieve and print the assistant's final response
    final_response = thread.get_final_response()
    print(final_response.text)"""

if __name__ == "__main__":
    main()