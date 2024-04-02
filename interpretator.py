CREATE_CELL   = "$"
NEXT_CELL     = "+"
PREVIOUS_CELL = "-"
START_LOOP    = "{"
END_LOOP      = "}"
PRINT         = "!"
INPUT         = "?"
SAVE_BITE     = ";"
SAVE_BIT      = ":"
NEXT_BIT      = ">"
PREVIOUS_BIT  = "<"

class Interpretator:
    def __init__(self, code: str):
        self.cells: list[str] = []
        self.code = code

        self.cellPos = 0
        self.bitPos = 0
        self.currentBite = ""
        self.currentBit = ""

        self.code = self.removeComments(self.code)
    
    def begin(self):
        self.interpret()
    
    def interpret(self, start_pos = 0, end_pos = -1):
        pos = start_pos

        for syb in self.code[start_pos:end_pos] if end_pos != -1 else self.code[start_pos:]:

            if syb in "01":
                self.currentBite += syb
                self.currentBit = syb

            if syb == CREATE_CELL:
                self.cells.append("00000000")

            elif syb == NEXT_CELL:
                self.cellPos = self.cellPos + 1 if self.cellPos + 1 <= len(self.cells) - 1 else 0
            elif syb == PREVIOUS_CELL:
                self.cellPos = max(0, self.cellPos - 1)
            
            elif syb == NEXT_BIT:
                self.bitPos = self.bitPos + 1 if self.bitPos + 1 <= len(self.cells[self.cellPos]) - 1 else 0
            elif syb == PREVIOUS_BIT:
                self.bitPos = max(0, self.bitPos - 1)
            
            elif syb == START_LOOP:
                endLoopFined = self.code.find(END_LOOP, pos, end_pos)

                if endLoopFined != -1:
                    while self.binaryToASCII(self.cells[self.cellPos]) != "0":
                        self.interpret(pos+1, endLoopFined)
                else:
                    print(f"BiLang : {pos} : Произошла ошибка, не удалось найти закрывающую скобку цикла.")
                    exit()
            
            elif syb == PRINT and self.cells[self.cellPos] != "00000000":
                print(self.binaryToASCII(self.cells[self.cellPos]), end = "", flush = True)
            elif syb == INPUT:
                data = input()
                if len(data) != 8 or not all(c in '01' for c in data):
                    print(f"BiLang : {pos} : Произошла ошибка при вводе текста : Значение \"{data}\" не корректное, должно быть бинарной строкой из 0 и 1.")
                    exit()

                self.cells[self.cellPos] = data
            
            elif syb == SAVE_BITE and self.currentBite != "":
                self.cells[self.cellPos] = self.currentBite
                self.currentBite = ""
            elif syb == SAVE_BIT and self.currentBit != "":
                self.cells[self.cellPos] = self.cells[self.cellPos][:self.bitPos] + self.currentBit  + self.cells[self.cellPos][self.bitPos + 1:]
                self.currentBit = ""

            if syb not in "01" and syb != SAVE_BIT and self.currentBit != "":
                self.currentBit = ""
            if syb not in "01" and syb != SAVE_BITE and self.currentBite != "":
                self.currentBite = ""
        
            pos += 1
    
    def removeComments(self, code: str):
        result = ""
        commentFound = False

        for char in code:
            if char == "@":
                commentFound = True
            elif char == "\n":
                commentFound = False
            elif not commentFound:
                result += char
        
        return result.replace(" ", "")
    
    def binaryToASCII(self, text: str):
        binary_list = text.split()
        ascii_result = ""
        for binary_num in binary_list:
            decimal_num = int(binary_num, 2)
            if 0 <= decimal_num <= 127:
                ascii_result += chr(decimal_num)
            else:
                return None
        return ascii_result