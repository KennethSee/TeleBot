import os
import telebot
from flask import Flask, request

from utils import add_score, reduce_score, get_ranking, add_to_group
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
    userid = message.from_user.id
    score = db.get_social_credit_score(userid)
    reply = f'{message.from_user.first_name}, you have a social credit of {score}. '
    if int(score) < 0:
        reply += 'Dishonorable.'
    elif int(score) > 1000:
        reply += 'The CCP thanks you for being a righteous citizen.'
    bot.send_message(message.chat.id, reply)

@bot.message_handler(func=lambda m: True, content_types=['sticker'])
def social_credit_counter(message):
    sticker = message.sticker
    reply = message.reply_to_message
    if sticker.set_name == 'PoohSocialCredit' and reply is not None:
        userid = reply.from_user.id
        name = reply.from_user.first_name
        chat_id = message.chat.id
        chat_name = message.chat.title

        # update chat members
        add_to_group(db, chat_id, chat_name, userid)

        # check if replying to self
        if message.from_user.id == reply.from_user.id:
            bot.send_message(message.chat.id, 'Influencing your own social score is not socially desirable behaviour. -20 points.')
            reduce_score(db, userid, name, 20)
        else:
            if sticker.emoji == '😄':
                add_score(db, userid, name, 20)
            elif sticker.emoji == '😞':
                reduce_score(db, userid, name, 20)
        # bot.reply_to(message, f'{name}, your social credit is now {db.get_social_credit_score(username)}')
        
@bot.message_handler(commands=['ranking'])
def ranking(message):
    chat_id = message.chat.id
    rankings = get_ranking(db, chat_id)
    bot.send_message(chat_id, rankings)

@bot.message_handler(commands=['urk'])
def urk(message):
    reply = message.reply_to_message
    if reply is not None:
        reply_user = reply.from_user.first_name
        bot.send_message(message.chat.id, f'{reply_user} needs a good hard URk!')
    bot.send_sticker(message.chat.id, 'CAACAgEAAxkBAAEDbDZhrh1hLCZQXI6vMa38t9HIjVcx5gACGgADPLOxB_ZVKFF6mQdnIgQ')

@bot.message_handler(func=lambda m: True, content_types=['text'])
def revolution(message):
    text = message.text.lower()
    if 'revolution' in text:
        bot.send_message(message.chat.id, 'Long live the revolution!')
    elif 'sorry i can\'t' in text or 'sorry i cannot' in text or 'can\'t make it' in text:
        bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAEDbtFhr30W6ds72yYsLX9EMixUsBXKhgAC8AIAAq1iKVcctN3YMdC8VSME')
    elif 'good morning' in text:
        bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAEDbtNhr37xYemxxip7fzivN1k3WAP6mAACfQYAArffewq76K5rz_X8qSME')
    elif ' pm ' in text:
        bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAEDbthhr385k2iDSbo6XI_oGaPoThcuHwACewYAArffewrF24jnUr4miyME')

# @bot.message_handler(func=lambda m: True, content_types=['text', 'sticker'])
# def test_channel(message):
#     print(message)

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

# bot.remove_webhook()
# bot.infinity_polling()