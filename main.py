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

line_bot_api = LineBotApi(str(config['line_bot']['Channel_Access_Token']))
handler = WebhookHandler(str(config['line_bot']['Channel_Secret']))

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
