import random
import json


class User:
    id = -1
    firstName = "None"
    grade = -1
    theme = ""
    gradeAVG = -1
    data = -1


class Lesson:
    user = User()
    userFile = "None"
    js = "None"

    def get_themes_list(self):
        # Выдать темы
        themes = []
        for i in self.js:
            themes.append(i["Theme"])
        return themes

    def start(self):
        # Открыть файл профиля
        directory = f"users/id{self.user.id}.json"
        self.userFile = open(directory, "r", encoding="utf-8")
        self.js = json.load(self.userFile)
        self.userFile.close()
        print(self.user.firstName, ", урок начался!")

    def end(self):
        # Закрыть и сохраненить файл профиля
        directory = f"users/id{self.user.id}.json"
        self.userFile = open(directory, "w", encoding="utf-8")
        json.dump(self.js, self.userFile, indent=4, ensure_ascii=False)
        self.userFile.close()
        print(self.user.firstName, ", урок закончился!")

    def set_theme(self, theme):
        pass

    def question(self):
        # Найти слова по теме
        words = []
        for i in self.js["progress"]:
            if i["Theme"] == self.js["theme"]:
                words = i["Words"]
                
        # Создать вопрос и варианты ответов
        random.shuffle(words)
        index = 0
        o = []
        for word in words:
            index += 1
            if word["grade"] < self.js["grade"]:
                q = f"Переведите: {word['EN']}"
                o.append(f"{word['EN']}: {word['RU']}")
                i = 1
                while i < self.js["complexity"]:
                    o.append(f"{word['EN']}: {words[(index + i + 2) % len(words)]['RU']}")
                    i += 1
                random.shuffle(o)
                res = {"Question": q, "Answer options": o}
                return res
        else:
            return -1

    def answer(self, en, ru):
        i = 0
        while i < len(self.js["progress"]):
            if self.js["progress"][i]["Theme"] == self.js["theme"]:
                j = 0
                while j < len(self.js["progress"][i]["Words"]):
                    if self.js["progress"][i]["Words"][j]["EN"] == en:
                        if self.js["progress"][i]["Words"][j]["RU"] == ru:
                            self.js["progress"][i]["Words"][j]["grade"] += 1
                            return "Угу"
                        else:
                            self.js["progress"][i]["Words"][j]["grade"] = 0
                            return "Неа"
                    j += 1
            i += 1
        return "Сам такой"
