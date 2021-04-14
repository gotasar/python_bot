import shutil
import telebot
from telebot import types
from keyboard import User, Lesson
from BotDataBase import BotDataBase
from lesson import LessonDB

TOKEN = '1671733318:AAGZe8uuEOkQtTwT8McKa9LyV5JhQGTwt5g'
bot = telebot.TeleBot(TOKEN)


class BotKeyboard:
    @staticmethod
    def start_keyboard():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn_start = types.KeyboardButton('Начать тест')
        btn_statistic = types.KeyboardButton('Статистика')
        btn_params = types.KeyboardButton('Настройка параметров')
        markup.add(btn_start)
        markup.add(btn_statistic)
        markup.add(btn_params)
        return markup

    @staticmethod
    def setting_keyboard():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        complexity_add = types.KeyboardButton('Увеличить сложность')
        complexity_sub = types.KeyboardButton('Уменьшить сложность')
        grade_add = types.KeyboardButton('Увеличить повторения')
        grade_sub = types.KeyboardButton('Уменьшить повторения')
        theme_options = types.KeyboardButton('Сменить тему')
        markup.add(complexity_add)
        markup.add(complexity_sub)
        markup.add(grade_add)
        markup.add(grade_sub)
        markup.add(theme_options)
        return markup

    @staticmethod
    def theme_keyboard(themes):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for theme in themes:
            theme_button = types.KeyboardButton(f'Тема: {theme}')
            markup.add(theme_button)
        return markup


class BotTranslate:
    @staticmethod
    def start(json):
        id = json['message']['chat']['id']
        fn = json['message']['chat']["first_name"]
        BotDataBase.add_user(id, fn)

        dir = f"id{id}"
        shutil.copyfile(r'words.json', f'users/{dir}.json')
        
        bot.send_message(id, "Пивет, ЧОРТ!", reply_markup=BotKeyboard.start_keyboard())

    @staticmethod
    def question(json):
        user_id = json['message']['chat']['id']
        BotDataBase.cur.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
        row = BotDataBase.cur.fetchone()
        q = LessonDB.question(row)
        if q != -1:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            print(q)
            for options in q["Answer options"]:
                markup.add(types.KeyboardButton(options))
            bot.send_message(user_id, q["Question"], reply_markup=markup)

        """
        user = User()
        user.id = json['message']['chat']['id']
        user.firstName = json['message']['chat']['first_name']
        lesson = Lesson()
        lesson.user = user

        chat_id = json['message']['chat']['id']

        lesson.start()
        q = lesson.question()
        if q != -1:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            print(q)
            for options in q["Answer options"]:
                markup.add(types.KeyboardButton(options))
            bot.send_message(chat_id, q["Question"], reply_markup=markup)
        lesson.end()
        """

    @staticmethod
    def answer(json, words):
        print(json)
        print(words)

        user = User()
        user.id = json['message']['chat']['id']
        user.firstName = json['message']['chat']['first_name']
        lesson = Lesson()
        lesson.user = user
        chat_id = json['message']['chat']['id']

        lesson.start()
        print(lesson.answer(words[0], words[1]))
        bot.send_message(chat_id, lesson.answer(words[0], words[1]), reply_markup=BotKeyboard.start_keyboard())
        print(lesson.js)
        lesson.end()
        pass

    @staticmethod
    def complexity_add(json, par):
        user = User()
        user.id = json['message']['chat']['id']
        user.firstName = json['message']['chat']['first_name']
        lesson = Lesson()
        lesson.user = user
        chat_id = json['message']['chat']['id']

        lesson.start()
        lesson.js["complexity"] += par
        if lesson.js["complexity"] < 3:
            lesson.js["complexity"] = 3
        if lesson.js["complexity"] > 5:
            lesson.js["complexity"] = 5
        bot.send_message(chat_id, "Сложность изменена", reply_markup=BotKeyboard.start_keyboard())
        lesson.end()

    @staticmethod
    def grade_add(json, par):
        user = User()
        user.id = json['message']['chat']['id']
        user.firstName = json['message']['chat']['first_name']
        lesson = Lesson()
        lesson.user = user
        chat_id = json['message']['chat']['id']

        lesson.start()
        lesson.js["grade"] += par
        if lesson.js["grade"] < 3:
            lesson.js["grade"] = 3
        if lesson.js["grade"] > 10:
            lesson.js["grade"] = 10
        bot.send_message(chat_id, "Количество повторений изменено", reply_markup=BotKeyboard.start_keyboard())
        lesson.end()

    @staticmethod
    def statistic(json):
        user = User()
        user.id = json['message']['chat']['id']
        user.firstName = json['message']['chat']['first_name']
        lesson = Lesson()
        lesson.user = user
        chat_id = json['message']['chat']['id']

        lesson.start()
        theme = f'Текущая тема: {lesson.js["theme"]}'
        #print(stat)
        complexity = f'Сложность: {lesson.js["complexity"] - 2}'
        #print(stat)
        grade = f'Количество повторений: {lesson.js["grade"]}'
        stat = theme + '\n' + complexity + '\n' + grade
        print(stat)
        bot.send_message(chat_id, stat, reply_markup=BotKeyboard.start_keyboard())
        lesson.end()

    @staticmethod
    def setting(json):
        user = User()
        user.id = json['message']['chat']['id']
        user.firstName = json['message']['chat']['first_name']
        lesson = Lesson()
        lesson.user = user
        chat_id = json['message']['chat']['id']

        lesson.start()
        bot.send_message(chat_id, "Настройки", reply_markup=BotKeyboard.setting_keyboard())
        lesson.end()

    @staticmethod
    def theme_options(json):
        user = User()
        user.id = json['message']['chat']['id']
        user.firstName = json['message']['chat']['first_name']
        lesson = Lesson()
        lesson.user = user
        chat_id = json['message']['chat']['id']

        lesson.start()
        themes = []
        for p in lesson.js["progress"]:
            themes.append(p["Theme"])
        bot.send_message(chat_id, "Выберите тему", reply_markup=BotKeyboard.theme_keyboard(themes))
        lesson.end()

    @staticmethod
    def switch_theme(json, theme):
        user = User()
        user.id = json['message']['chat']['id']
        user.firstName = json['message']['chat']['first_name']
        lesson = Lesson()
        lesson.user = user
        chat_id = json['message']['chat']['id']

        lesson.start()
        themes = []
        for p in lesson.js["progress"]:
            themes.append(p["Theme"])
        if theme in themes:
            lesson.js["theme"] = theme
            bot.send_message(chat_id, "Тема изменена", reply_markup=BotKeyboard.start_keyboard())
        else:
            bot.send_message(chat_id, "Такой темы нет", reply_markup=BotKeyboard.start_keyboard())
        lesson.end()

