import json
import openai

from config import open_api_config, line_config
from flask import Flask, request
# from flask_ngrok import run_with_ngrok

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage

app = Flask(__name__)
# run_with_ngrok(app)


openai.organization = open_api_config['org']
openai.api_key = open_api_config['key']


def get_gpt_response(text: str):
    result = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'user',
                'content': text
            }
        ]
    )
    return result.choices[0].message['content']


@app.route('/', methods=['POST'])
def bot():
    data = request.get_data(as_text=True)
    try:
        json_data = json.loads(data)
        bot_api = LineBotApi(line_config['token'])

        handler = WebhookHandler(line_config['secret'])
        signature = request.headers['X-Line-Signature']
        handler.handle(data, signature)

        my_event = json_data['events'][0]
        event_message = my_event['message']
        type = event_message['type']

        if type == 'text':
            message = event_message['text']
        elif type == 'sticker':
            sticker_keywords = event_message['keywords'][0]
            message = sticker_keywords
        else:
            message = 'say I support text messages only'

        message = get_gpt_response(message)
        reply_token = my_event['replyToken']
        bot_api.reply_message(reply_token, TextSendMessage(message))
    except InvalidSignatureError:
        print('line invalid signature')
    except Exception as ex:
        print('UNKNOWN EXCEPTION', ex)

    return 'OK'


@app.route('/', methods=['GET'])
def hello():
    return '<h1>200</h1>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
