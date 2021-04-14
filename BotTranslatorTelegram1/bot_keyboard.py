from telebot import types
from tb_static import TB
from db_static import DB

bot = TB.get()
conn = DB.get()


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
