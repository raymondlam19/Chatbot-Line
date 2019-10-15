import configparser

from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Initial Flask app
app = Flask(__name__)

# Initial bot by line access token & secret
# line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
# handler = WebhookHandler(config['line_bot']['Channel_Secret'])

line_bot_api = LineBotApi('NVNdHbGiIF3VWfisbHk7zA5Kh6hZRtJBc0jpDa+qwqfTKlavJTstVB3vI/LA5pP/qJcnk880aBtIZXH+IfiE9TqgUzfkSLEIWAKbDG9F62aOA4y9rDDpBgsPoMn51+ixuT3rl6V2HZWu4i+CxeES0gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e3d4d7db066491a959a60a7ac52cd6b9')

@app.route("/callback", methods=['POST'])
def callback():

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print ("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    # Olami nlp
    #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=Olami().nli(event.message.text,event.source.user_id)))

# Running server
if __name__ == "__main__":
    app.run(debug=True)
