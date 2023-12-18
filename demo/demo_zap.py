import os
from GPTPlugins4All.config import Config  # Replace with actual import paths
from GPTPlugins4All.assistant import Assistant

from dotenv import load_dotenv
load_dotenv()


config5 = Config('Zapier2')
print(config5.spec_object)
print(config5.spec_string)


config5.add_auth_method("HEADER", {"header_name": "x-api-key", "key": os.getenv('ZAPIER_KEY')})
request = config5.make_api_call_by_operation_id("list_exposed_actions", params={})
print(request)
print(request.json())
config5.is_json = True
assistant = Assistant(config5, "Zapier Assistant", "You are an assistant who helps users through Zapier. ", "gpt-4-1106-preview")


if __name__ == '__main__':
    while True:
        user_input = input("Enter your message: ")
        response = assistant.get_assistant_response(user_input)
        print(response)