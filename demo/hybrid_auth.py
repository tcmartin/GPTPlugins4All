import os
from GPTPlugins4All.config import Config  # Replace with actual import paths
from GPTPlugins4All.assistant import Assistant

from dotenv import load_dotenv
load_dotenv()



from flask import Flask, request, jsonify
app = Flask(__name__)

config5 = Config('sheets_fun')
config5.is_json = True
config2 = Config('sendgrid')
config2.add_auth_method("HEADER", {"header_name": "Authorization", "key": "Bearer "+os.getenv('SENDGRID_KEY')})
config2.is_json = True
config5.add_auth_method("OAUTH", {
    "response_type": "code",
    "auth_url": "https://accounts.google.com/o/oauth2/auth",
    "token_url": "https://oauth2.googleapis.com/token",
    "client_id": os.getenv('GOOGLE_CLIENT_ID'),
    "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
    "redirect_uri": "http://localhost:8000/",
    "scope": "https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/drive"
})
assistant = Assistant([config2, config5], "Sheet Assistant", "You are an assistant who helps users manage google sheets. You can also send emails", "gpt-4-1106-preview")
callback = None
@app.route('/')
def oauth_callback():
    # Extract the code or token from the request
    global callback
    code = request.args.get('code')
    token = request.args.get('token')  # Depending on the OAuth flow

    # Here you'd typically exchange the code for a token if you received a code
    # For simplicity, this example just returns the received code or token

    # Return the code or token as a JSON response
    print(code)
    callback = config5.handle_oauth_callback(code)
    return jsonify({
        "code": code
    })
@app.route('/get_assistant_response', methods=['POST'])
def get_assistant_response_():
    user_input = request.json['message']
    response = assistant.get_assistant_response(user_input, {'sheets_fun':callback})
    return jsonify(response)
@app.route('/get_assistant_response', methods=['GET'])
def get_assistant_response__():
    user_input = request.args.get('message')
    response = assistant.get_assistant_response(user_input, {'sheets_fun':callback})
    return jsonify(response)

if __name__ == '__main__':
    print(config5.start_oauth_flow())
    app.run(debug=True, port=8000)