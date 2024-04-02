from interpreter import Interpreter

code: str = ""

with open("code.bl", "r", encoding = "utf-8") as file:
    code = file.read()

BiLang = Interpreter(code)
BiLang.begin()