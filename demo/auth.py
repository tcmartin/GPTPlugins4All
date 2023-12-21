import os
from GPTPlugins4All.config import Config  # Replace with actual import paths
from GPTPlugins4All.assistant import Assistant

from dotenv import load_dotenv
load_dotenv()



from flask import Flask, request, jsonify
app = Flask(__name__)
spec5 = '''
{
  "openapi": "3.1.0",
  "info": {
    "title": "Google sheets",
    "description": "Views, edits, creates Google sheets",
    "version": "v0.0.1"
  },
  "servers": [
    {
      "url": "https://sheets.googleapis.com/v4"
    }
  ],
  "paths": {
    "/spreadsheets": {
      "post": {
        "description": "Create a new spreadsheet",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Spreadsheet"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Spreadsheet created successfully",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Spreadsheet"
                }
              }
            }
          }
        },
        "security": [
          {
            "oauth2": []
          }
        ]
      }
    },
    "/spreadsheets/{spreadsheetId}": {
      "get": {
        "description": "Retrieve spreadsheet details",
        "parameters": [
          {
            "name": "spreadsheetId",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Details of the requested spreadsheet",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Spreadsheet"
                }
              }
            }
          }
        },
        "security": [
          {
            "oauth2": []
          }
        ]
      }
    },
    "/spreadsheets/{spreadsheetId}/values/{range}": {
      "get": {
        "description": "Read spreadsheet values",
        "parameters": [
          {
            "name": "spreadsheetId",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "range",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Values read successfully",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ValueRange"
                }
              }
            }
          }
        },
        "security": [
          {
            "oauth2": []
          }
        ]
      }
    },
    "/spreadsheets/{spreadsheetId}:batchUpdate": {
      "post": {
        "description": "Apply multiple updates to a spreadsheet in one request",
        "parameters": [
          {
            "name": "spreadsheetId",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/BatchUpdateRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Batch update applied successfully",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/BatchUpdateResponse"
                }
              }
            }
          }
        },
        "security": [
          {
            "oauth2": []
          }
        ]
      }
    }
  },
  "components": {
    "schemas": {
      "BatchUpdateRequest": {
        "type": "object",
        "properties": {
          "requests": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/BatchUpdateRequestItem"
            }
          }
        }
      },
      "BatchUpdateRequestItem": {
        "type": "object",
        "properties": {
          "updateId": {
            "type": "string"
          },
          "updateType": {
            "type": "string"
          },
          "range": {
            "type": "string"
          },
          "values": {
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "type": "object"
              }
            }
          }
        }
      },
      "BatchUpdateResponse": {
        "type": "object",
        "properties": {
          "spreadsheetId": {
            "type": "string"
          },
          "responses": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/BatchUpdateResponseItem"
            }
          }
        }
      },
      "BatchUpdateResponseItem": {
        "type": "object",
        "properties": {
          "updateId": {
            "type": "string"
          },
          "updateStatus": {
            "type": "string"
          }
        }
      },
      "Spreadsheet": {
        "type": "object",
        "properties": {
          "spreadsheetId": {
            "type": "string"
          },
          "properties": {
            "$ref": "#/components/schemas/SpreadsheetProperties"
          },
          "sheets": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Sheet"
            }
          }
        }
      },
      "SpreadsheetProperties": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string"
          }
        }
      },
      "Sheet": {
        "type": "object",
        "properties": {
          "properties": {
            "$ref": "#/components/schemas/SheetProperties"
          }
        }
      },
      "SheetProperties": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string"
          }
        }
      },
      "ValueRange": {
        "type": "object",
        "properties": {
          "range": {
            "type": "string"
          },
          "majorDimension": {
            "type": "string"
          },
          "values": {
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "type": "object"
              }
            }
          }
        }
      }
    }
  }
}
'''
config5 = Config(spec5, name='google_sheets')
print(config5.spec_object)
print(config5.spec_string)
config5.is_json = True
config5.add_auth_method("OAUTH", {
    "response_type": "code",
    "auth_url": "https://accounts.google.com/o/oauth2/auth",
    "token_url": "https://oauth2.googleapis.com/token",
    "client_id": os.getenv('GOOGLE_CLIENT_ID'),
    "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
    "redirect_uri": "http://localhost:8000/",
    "scope": "https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/drive"
})
assistant = Assistant(config5, "Sheet Assistant", "You are an assistant who helps users manage google sheets. ", "gpt-4-1106-preview")
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
    print(user_input)
    response = assistant.get_assistant_response(user_input, {'google_sheets':callback})
    return jsonify(response)
@app.route('/get_assistant_response', methods=['GET'])
def get_assistant_response__():
    user_input = request.args.get('message')
    print(user_input)
    print(callback)
    response = assistant.get_assistant_response(user_input, {'google_sheets':callback})
    return jsonify(response)

if __name__ == '__main__':
    print(config5.start_oauth_flow())
    app.run(debug=True, port=8000)