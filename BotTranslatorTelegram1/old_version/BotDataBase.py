# web: gunicorn main:app
# worker: python main.py 5000
# heroku addons:create heroku-postgresql:hobby-dev
# Created postgresql-metric-65240 as DATABASE_URL
# pip install psycopg2-binary
# heroku ps:scale web=1
# heroku logs --tail

# import os
import psycopg2
from datetime import datetime
import json

class BotDataBase:
    conn = -1
    cur = -1

    @staticmethod
    def connect():
        # DATABASE_URL = os.environ['postgresql-metric-65240']
        # BotDataBase.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        BotDataBase.conn = psycopg2.connect(database="dfh4u9ku9r591a",
                                            user="pihbteuhurzhje",
                                            password="0318a7704a9234b8744cba962b1b1a63b919d5a87d4810b4810f299794749ae8",
                                            host="ec2-52-71-161-140.compute-1.amazonaws.com",
                                            port=5432)
        BotDataBase.cur = BotDataBase.conn.cursor()
        pass

    @staticmethod
    def tb_users():
        BotDataBase.cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, " +
                                "first_name VARCHAR(64), " +
                                "state INTEGER," +
                                "theme INTEGER," +
                                "complexity INTEGER," +
                                "grade INTEGER," +
                                "num_questions INTEGER," +
                                "last_date timestamp," +
                                "max_question INTEGER," +
                                "word INTEGER," +
                                "rating INTEGER)")
        BotDataBase.conn.commit()

    @staticmethod
    def tb_themes():
        BotDataBase.cur.execute("CREATE TABLE themes (id SERIAL PRIMARY KEY, " +
                                "theme VARCHAR(64))")
        BotDataBase.conn.commit()

    @staticmethod
    def tb_words():
        BotDataBase.cur.execute("CREATE TABLE words (id SERIAL PRIMARY KEY, " +
                                "theme INTEGER, " +
                                "en VARCHAR(64), " +
                                "ru VARCHAR(64))")
        BotDataBase.conn.commit()

    @staticmethod
    def tb_states():
        BotDataBase.cur.execute("CREATE TABLE states (id SERIAL PRIMARY KEY, " +
                                "state INTEGER)")
        BotDataBase.conn.commit()

    @staticmethod
    def tb_progress():
        BotDataBase.cur.execute("CREATE TABLE progress (id SERIAL PRIMARY KEY, " +
                                "user_id INTEGER, " +
                                "word INTEGER, " +
                                "grade INTEGER, " +
                                "last_date timestamp)")
        BotDataBase.conn.commit()

    @staticmethod
    def add_user(id, first_name):
        cur = BotDataBase.conn.cursor()
        cur.execute(f"SELECT * FROM users WHERE id = {id}")
        row = cur.fetchone()
        if row is None:
            return
        cur.execute("INSERT INTO users (id, first_name, state, theme, complexity, grade, num_questions) " +
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (id, first_name, 1, 1, 3, 3, 3))
        BotDataBase.conn.commit()
        cur.execute("SELECT id FROM words")
        for row in cur:
            word_id = row[0]
            print(word_id)
            user_id = id
            BotDataBase.add_progress(user_id, word_id)
        cur.execute("SELECT * FROM users")
        for row in cur:
            print(row)

    @staticmethod
    def add_theme(theme):
        cur = BotDataBase.conn.cursor()
        cur.execute("INSERT INTO themes (theme) " +
                    "VALUES (%s)",
                    (theme, ))
        BotDataBase.conn.commit()

    @staticmethod
    def add_word(theme, en, ru):
        cur = BotDataBase.conn.cursor()
        cur.execute("INSERT INTO words (theme, en, ru) " +
                    "VALUES (%s, %s, %s)",
                    (theme, en, ru))
        BotDataBase.conn.commit()
        cur.execute("SELECT * FROM words")
        for row in BotDataBase.cur:
            print(row)

    @staticmethod
    def add_progress(user, word):
        cur = BotDataBase.conn.cursor()
        cur.execute("INSERT INTO progress (user_id, word, grade, last_date) " +
                    "VALUES (%s, %s, %s, %s)",
                    (user, word, 0, datetime.now()))
        BotDataBase.conn.commit()

    @staticmethod
    def add_themes_and_words(dir):
        with open(dir, "r", encoding="utf-8") as f:
            js = json.load(f)
            themes = []
            for p in js["progress"]:
                print(p["Theme"])
                print(type(p["Theme"]))
                theme = str(p["Theme"])
                BotDataBase.add_theme(theme)
                BotDataBase.cur.execute(f"SELECT id FROM themes WHERE theme = '{theme}'")
                row = BotDataBase.cur.fetchone()
                theme_id = row[0]
                for word in p["Words"]:
                    print(word)
                    BotDataBase.add_word(theme_id, word['EN'], word['RU'])

    @staticmethod
    def init():
        BotDataBase.tb_users()
        BotDataBase.tb_words()
        BotDataBase.tb_states()
        BotDataBase.tb_themes()
        BotDataBase.tb_progress()
        BotDataBase.add_themes_and_words('words.json')

"""
class BotDataBase:
    conn = -1
    cur = -1

    @staticmethod
    def connect():
        # DATABASE_URL = os.environ['postgresql-metric-65240']
        # BotDataBase.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        BotDataBase.conn = psycopg2.connect(database="dfh4u9ku9r591a",
                                            user="pihbteuhurzhje",
                                            password="0318a7704a9234b8744cba962b1b1a63b919d5a87d4810b4810f299794749ae8",
                                            host="ec2-52-71-161-140.compute-1.amazonaws.com",
                                            port=5432)
        BotDataBase.cur = BotDataBase.conn.cursor()
        pass

    @staticmethod
    def tb_users():  # Modify
        BotDataBase.cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, " +
                                "first_name VARCHAR(64), " +
                                "state INTEGER," +
                                "theme INTEGER," +
                                "complexity INTEGER," +
                                "grade INTEGER," +
                                "num_questions INTEGER)")
        BotDataBase.conn.commit()

    @staticmethod
    def tb_themes():
        BotDataBase.cur.execute("CREATE TABLE themes (id SERIAL PRIMARY KEY, " +
                                "theme VARCHAR(64))")
        BotDataBase.conn.commit()

    @staticmethod
    def tb_words():
        BotDataBase.cur.execute("CREATE TABLE words (id SERIAL PRIMARY KEY, " +
                                "theme INTEGER, " +
                                "en VARCHAR(64), " +
                                "ru VARCHAR(64))")
        BotDataBase.conn.commit()

    @staticmethod
    def tb_states():  # Delete
        BotDataBase.cur.execute("CREATE TABLE states (id SERIAL PRIMARY KEY, " +
                                "state INTEGER)")
        BotDataBase.conn.commit()

    @staticmethod
    def tb_progress():
        BotDataBase.cur.execute("CREATE TABLE progress (id SERIAL PRIMARY KEY, " +
                                "user_id INTEGER, " +
                                "word INTEGER, " +
                                "grade INTEGER, " +
                                "last_date timestamp)")
        BotDataBase.conn.commit()

    @staticmethod
    def add_user(json):
        id = json['message']['chat']['id']
        first_name = json['message']['chat']['first_name']
        BotDataBase.cur.execute("INSERT INTO users (id, first_name, state, theme, complexity, grade, num_questions) " +
                                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (id, first_name, -1, 1, 3, 3, 3))
        BotDataBase.conn.commit()
        BotDataBase.cur.execute("SELECT id FROM words")
        for row in BotDataBase.cur:
            user = id
            word = row[0]
            BotDataBase.add_progress(user, word)

    @staticmethod
    def add_theme(theme):
        BotDataBase.cur.execute("INSERT INTO themes (theme) " +
                                "VALUES (%s)",
                                (theme, ))
        BotDataBase.conn.commit()

    @staticmethod
    def add_word(theme, en, ru):
        BotDataBase.cur.execute("INSERT INTO words (theme, en, ru) " +
                                "VALUES (%s, %s, %s)",
                                (theme, en, ru))
        BotDataBase.conn.commit()

    @staticmethod
    def add_progress(user, word):
        BotDataBase.cur.execute("INSERT INTO progress (user_id, word, grade, last_date) " +
                                "VALUES (%s, %s, %s, %s)",
                                (user, word, 0, datetime.today()))
        BotDataBase.conn.commit()

    @staticmethod
    def add_themes_and_words(dir):
        with open(dir, "r", encoding="utf-8") as f:
            js = json.load(f)
            themes = []
            for p in js["progress"]:
                print(p["Theme"])
                print(type(p["Theme"]))
                theme = str(p["Theme"])
                BotDataBase.add_theme(theme)
                BotDataBase.cur.execute(f"SELECT id FROM themes WHERE theme = '{theme}'")
                row = BotDataBase.cur.fetchone()
                theme_id = row[0]
                for word in p["Words"]:
                    print(word)
                    BotDataBase.add_word(theme_id, word['EN'], word['RU'])

    @staticmethod
    def init():
        BotDataBase.tb_users()
        BotDataBase.tb_words()
        BotDataBase.tb_states()
        BotDataBase.tb_themes()
        BotDataBase.tb_progress()
        BotDataBase.add_themes_and_words('words.json')
"""
