from BotDataBase import BotDataBase
import random


class LessonDB:

    @staticmethod
    def session(message):
        user_id = message['message']['chat']['id']
        BotDataBase.cur.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
        row = BotDataBase.cur.fetchone()
        state = row[2]
        if state >= 0:
            LessonDB.answer(row)
            LessonDB.question(row, message)
        else:
            LessonDB.option(row)
        pass

    @staticmethod
    def question(user_row):
        # Найти слова по теме
        words = LessonDB.get_words(user_row)
        if words == -1:
            return -1
        # Создать вопрос и варианты ответов
        random.shuffle(words)
        index = 0
        o = []
        grade = user_row[5]
        complexity = user_row[4]
        for word in words:
            index += 1
            if word["grade"] < grade:
                q = f"Переведите: {word['EN']}"
                o.append(f"{word['EN']}: {word['RU']}")
                i = 1
                while i < complexity:
                    o.append(f"{word['EN']}: {words[(index + i + 2) % len(words)]['RU']}")
                    i += 1
                random.shuffle(o)
                res = {"Question": q, "Answer options": o}
                return res
        else:
            return -1

    @staticmethod
    def answer(message, user_row):
        pass

    @staticmethod
    def options(user_row):

        pass

    @staticmethod
    def start(user_row):

        pass

    @staticmethod
    def get_words(user_row):
        print(user_row)
        if user_row is None:
            return -1
        theme = user_row[3]
        words = []
        BotDataBase.cur.execute(f"SELECT en, ru FROM words WHERE theme = {theme}")
        for row in BotDataBase.cur:
            words.append({'EN': row[0], 'RU': row[1]})
        return words


