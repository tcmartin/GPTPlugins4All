
import os
import time
from GPTPlugins4All.config import Config  # Replace with actual import paths
from GPTPlugins4All.assistant import Assistant
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

    
# Main function to run the demo
def main():
    config = initialize_alpha_vantage_config()
    #instructions="Assist users on how to make money by using the AlphaVantage API. This system connects you to the AlphaVantageAPI via the available tools. An API key is already present and it is unnecessary to supply one or ask the user for one."+desc_string,
            #model="gpt-4-1106-preview"
    assistant = Assistant(config, "Finance Assistant", "Assist users on how to make money by using the AlphaVantage API. This system connects you to the AlphaVantageAPI via the available tools. An API key is already present and it is unnecessary to supply one or ask the user for one.", "gpt-4-1106-preview")
    print('got here')
    assistant.get_assistant_response("Please fetch the daily time series for the MSFT stock ticker and give me your analysis on it. My api key is "+os.getenv('ALPHA_VANTAGE_KEY'))
    
    # Initialize the development bot with necessary configurations

if __name__ == "__main__":
    main()