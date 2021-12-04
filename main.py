import os
import telebot
from flask import Flask, request

from storage import add_score, reduce_score
from db import DB


API_KEY = os.getenv('API_KEY')
PORT = int(os.environ.get('PORT', 5000))
bot = telebot.TeleBot(API_KEY)
db = DB('urkmebot-firebase-adminsdk-ezt3s-c8553cf80a.json')
server = Flask(__name__)


@bot.message_handler(commands=['greet'])
def greet(message):
    bot.send_message(message.chat.id, 'URk all of you!')

@bot.message_handler(commands=['myscore'])
def myscore(message):
    username = message.from_user.username
    score = db.get_social_credit_score(username)
    reply = f'{message.from_user.first_name}, you have a credit score of {score}. '
    if score < 0:
        reply += 'Dishonorable.'
    elif score > 1000:
        reply += 'The CCP thanks you for being a righteous citizen.'
    bot.send_message(message.chat.id, reply)

@bot.message_handler(func=lambda m: True, content_types=['sticker'])
def social_credit_counter(message):
    sticker = message.sticker
    reply = message.reply_to_message
    if sticker.set_name == 'PoohSocialCredit' and reply is not None:
        username = reply.from_user.username
        name = reply.from_user.first_name
        if sticker.emoji == '😄':
            add_score(db, username, name, 20)
        elif sticker.emoji == '😞':
            reduce_score(db, username, name, 20)
        bot.reply_to(message, f'{name}, your social credit is now {db.get_social_credit_score(username)}')

@server.route('/' + API_KEY, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://lit-cliffs-68545.herokuapp.com/' + API_KEY)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
