from interpretator import Interpretator

code: str = ""

with open("code.bl", "r", encoding = "utf-8") as file:
    code = file.read()

BiLang = Interpretator(code)
BiLang.begin()