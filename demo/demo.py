
import os
from GPTPlugins4All.config import Config  # Replace with actual import paths
from GPTPlugins4All.assistant import Assistant

from dotenv import load_dotenv
load_dotenv()


    
# Main function to run the demo
def main():
    config = Config('alpha_vantage')
    config.add_auth_method("QUERY", {"param_name": "apikey", "key": os.getenv('ALPHA_VANTAGE_KEY')})
    assistant = Assistant(config, "Finance Assistant", "Assist users on how to make money by using the AlphaVantage API. This system connects you to the AlphaVantageAPI via the available tools. An API key is already present and it is unnecessary to supply one or ask the user for one.", "gpt-4-1106-preview")
    assistant.get_assistant_response("Please fetch the daily time series for the MSFT stock ticker and give me your analysis on it. My api key is "+os.getenv('ALPHA_VANTAGE_KEY'))
if __name__ == "__main__":
    main()