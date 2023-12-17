
import os
from GPTPlugins4All.config import Config  # Replace with actual import paths
from GPTPlugins4All.assistant import Assistant

from dotenv import load_dotenv
load_dotenv()


    
# Main function to run the demo
def main():

    config2 = Config('sendgrid')

    config2.add_auth_method("HEADER", {"header_name": "Authorization", "key": "Bearer "+os.getenv('SENDGRID_KEY')})
    config2.is_json = True
    assistant = Assistant([config2], "Email Assistant", "Assist users with emails. This system connects you to the SendGrid API so you can send emails. SendGrid requires json. You can directly call the api through this system. Attempt to use it as much as possible to assist the user.", "gpt-4-1106-preview")
    #assistant = Assistant([config, config2], "Finance Assistant", "Assist users on how to make money by using the AlphaVantage API. This system connects you to the AlphaVantageAPI via the available tools. This system also connects you Giphy to get gifs. Attempt to use them as much as possible to assist the user.", "gpt-4-1106-preview")
    assistant.get_assistant_response("Please send an email to me about the power of AI in marketing. Use my email for both sender and recipient. My email is "+os.getenv('EMAIL'))
    while True:
        user_input = input("Enter your message: ")
        assistant.get_assistant_response(user_input)
if __name__ == "__main__":
    main()