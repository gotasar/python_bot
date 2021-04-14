import telebot


class TB:
    bot = None

    @staticmethod
    def get():
        if TB.bot is None:
            token = '1610355784:AAHUz0b-GSk8iOlwlrR0jiLTkAeXYEOcw1M'
            TB.bot = telebot.TeleBot(token)
        return TB.bot