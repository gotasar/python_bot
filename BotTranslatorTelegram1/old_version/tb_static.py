import telebot


class TB:
    bot = None

    @staticmethod
    def bot():
        if TB.bot is None:
            token = '1671733318:AAGZe8uuEOkQtTwT8McKa9LyV5JhQGTwt5g'
            TB.bot = telebot.TeleBot(token)
        return TB.bot