
import os
from GPTPlugins4All.config import Config  # Replace with actual import paths
from GPTPlugins4All.assistant import Assistant

from dotenv import load_dotenv
load_dotenv()


    
# Main function to run the demo
def main():
    config = Config('alpha_vantage')
    config.add_auth_method("QUERY", {"param_name": "apikey", "key": os.getenv('ALPHA_VANTAGE_KEY')})
    config2 = Config('sendgrid')
    config2.is_json = True
    #config2 = Config('GifApi')
    config2.add_auth_method("HEADER", {"header_name": "Authorization", "key": "Bearer "+os.getenv('SENDGRID_KEY')})
    assistant = Assistant([config, config2], "Finance Assistant", "Assist users on how to make money by using the AlphaVantage API. This system connects you to the AlphaVantageAPI via the available tools. This system also connects you to the SendGrid API so you can send emails. SendGrid requires json while alphavantage doesn You can directly call the apis through this system. Attempt to use them as much as possible to assist the user.", "gpt-4-1106-preview")
    #assistant = Assistant([config, config2], "Finance Assistant", "Assist users on how to make money by using the AlphaVantage API. This system connects you to the AlphaVantageAPI via the available tools. This system also connects you Giphy to get gifs. Attempt to use them as much as possible to assist the user.", "gpt-4-1106-preview")
    assistant.get_assistant_response("Please fetch the daily time series for the MSFT stock ticker and give me your analysis on it. I would also like to receive an email report on this. Please send the email report to me immediately after getting the data and before replying. You can use my email as the from email as well. My email is "+os.getenv('EMAIL')+". My AlphaVantage api key is "+os.getenv('ALPHA_VANTAGE_KEY'))
    #get user input and send to assistant in a loop
    #assistant.get_assistant_response("Please look up Googles price history and find appropriate gifs to show how it's going. My AlphaVantage api key is "+os.getenv('ALPHA_VANTAGE_KEY'))
    while True:
        user_input = input("Enter your message: ")
        assistant.get_assistant_response(user_input)
if __name__ == "__main__":
    main()