# https://api.telegram.org/bot1671733318:AAGZe8uuEOkQtTwT8McKa9LyV5JhQGTwt5g/setWebhook?url=https://thawing-badlands-72124.herokuapp.com/
# ssh -R 80:localhost:5000 localhost.run

from flask import Flask, request, jsonify
import requests
import json
# import telebot
# from telebot import types
# from keyboard import User, Lesson
# import shutil
from translate_bot import BotTranslate, BotKeyboard
from BotDataBase import BotDataBase
# from lesson import LessonDB

from tb_static import TB
from db_static import DB

bot = TB.bot()
conn = DB.conn()
app = Flask(__name__)

# URL = 'https://api.telegram.org/bot1671733318:AAGZe8uuEOkQtTwT8McKa9LyV5JhQGTwt5g/'


@app.route('/', methods=['POST', 'GET'])
def index():
    i = 0

    if request.method == 'POST':

        r = request.get_json()
        chat_id = r['message']['chat']['id']

        if 'text' not in r['message']:
            bot.send_message(chat_id, "Опять за старое взялся?", reply_markup=BotKeyboard.start_keyboard())
            return jsonify(r)

        message = r['message']['text']
        if 'Начать тест' in message:
            BotDataBase.connect()
            BotTranslate.question(r)
        elif 'Статистика' in message:
            BotTranslate.statistic(r)
            pass
        elif 'Настройка параметров' in message:
            BotTranslate.setting(r)
            pass
        elif 'Увеличить сложность' in message:
            BotTranslate.complexity_add(r, 1)
            pass
        elif 'Уменьшить сложность' in message:
            BotTranslate.complexity_add(r, -1)
            pass
        elif 'Увеличить повторения' in message:
            BotTranslate.grade_add(r, 1)
            pass
        elif 'Уменьшить повторения' in message:
            BotTranslate.grade_add(r, -1)
            pass
        elif 'Сменить тему' in message:
            BotTranslate.theme_options(r)
            pass
        elif 'Тема: ' in message:
            words = message.split()
            if len(words) == 2:
                BotTranslate.switch_theme(r, words[1])
            pass
        elif '/start' == message:
            # BotDataBase.connect()
            # BotDataBase.tb_users()
            BotTranslate.start(r)
        elif 'Создай стартовую бд' == message:
            BotDataBase.connect()
            BotDataBase.init()
        else:
            words = message.split(': ')
            if len(words) == 2:
                BotTranslate.answer(r, words)
            else:
                bot.send_message(chat_id, "ЧТО-ТО НЕ ТАК!", reply_markup=BotKeyboard.start_keyboard())
        pass
        return jsonify(r)
    return '<h1> This is end <h1>'


if __name__ == '__main__':
    # BotDataBase.connect()
    # BotDataBase.init()
    app.run()

