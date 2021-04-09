import random

UKR = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
UKR_LEN = len(UKR)
EN = "abcdefghijklmnopqrstuvwzyx"
EN_LEN = len(EN)

def encrypt():
    language = input("Введiть мову: ")
    openText = input("Введiть відкритий текст: ")
    if language == "ukr":
        key = "".join(random.sample(UKR, len(openText.replace(" ", "").replace(",", "").replace(".", ""))))
        specialSymbols = [(i, openText[i]) for i in range(len(openText)) if openText[i] not in UKR]
    else:
        key = "".join(random.sample(EN, len(openText.replace(" ", "").replace(",", "").replace(".", ""))))
        specialSymbols = [(i, openText[i]) for i in range(len(openText)) if openText[i] not in EN]
    
    print(f"Ваш ключ: {key}")
    encryptedText = ""
    for i, j in zip(openText.replace(" ", "").replace(",", "").replace(".", ""), key):
        if language == "ukr":
            if UKR.index(i) + UKR.index(j) < UKR_LEN:
                encryptedText += UKR[(UKR.index(i) + UKR.index(j))]
            else:
                encryptedText += UKR[(UKR.index(i) + UKR.index(j)) - UKR_LEN]
            print(f"({i}, {j}) - ({UKR.index(i)}, {UKR.index(j)})")
        else:
            if EN.index(i) + EN.index(j) < EN_LEN:
                encryptedText += EN[(EN.index(i) + EN.index(j))]
            else:
                encryptedText += EN[(EN.index(i) + EN.index(j)) - EN_LEN]
            print(f"({i}, {j}) - ({EN.index(i)}, {EN.index(j)})")
    encryptedText = list(encryptedText)
    for specialSymbol in specialSymbols:
        encryptedText.insert(specialSymbol[0], specialSymbol[1])
    encryptedText = "".join(encryptedText)
    print(f"Зашифрований текст: {encryptedText}")
    with open("file.txt", "w") as file:
        file.write(key.encode("utf8").decode("cp1251"))
        file.write("\n".encode("utf8").decode("cp1251"))
        file.write(encryptedText.encode("utf8").decode("cp1251"))
        file.write("\n".encode("utf8").decode("cp1251"))
        file.write(language.encode("utf8").decode("cp1251"))


def decrypt():
    with open("file.txt", "r") as file:
        key = file.readline().replace("\n", "").encode("cp1251").decode("utf8")
        encryptedText = file.readline().replace("\n", "").encode("cp1251").decode("utf8")
        language = file.readline().replace("\n", "").encode("cp1251").decode("utf8")
    if language == "ukr":
        specialSymbols = [(i, encryptedText[i]) for i in range(len(encryptedText)) if encryptedText[i] not in UKR]
    else:
        specialSymbols = [(i, encryptedText[i]) for i in range(len(encryptedText)) if encryptedText[i] not in EN]
    decryptKey = []
    for i in key:
        if language == "ukr":
            decryptKey.append(UKR[UKR_LEN-UKR.index(i)])
        else:
            decryptKey.append(EN[EN_LEN-EN.index(i)])
    decryptedText = []
    for i, j in zip(encryptedText.replace(" ", "").replace(",", "").replace(".", ""), decryptKey):
        if language == "ukr":
            if UKR.index(i) + UKR.index(j) < UKR_LEN:
                decryptedText.append(UKR[(UKR.index(i) + UKR.index(j))])
            else:
                decryptedText.append(UKR[(UKR.index(i) + UKR.index(j)) - UKR_LEN])
        else:
            if EN.index(i) + EN.index(j) < EN_LEN:
                decryptedText.append(EN[(EN.index(i) + EN.index(j))])
            else:
                decryptedText.append(EN[(EN.index(i) + EN.index(j)) - EN_LEN])
    for specialSymbol in specialSymbols:
        decryptedText.insert(specialSymbol[0], specialSymbol[1])
    decryptedText = "".join(decryptedText)
    print(f"Розшифрований текст: {decryptedText}")


def loop():
    print("-"*16 + "┐\n1. Зашифрувати  |\n2. Розшифрувати |\n" + "-"*16 + "┘")
    choice = input("ВАШ ВИБІР: ")
    while choice in ["1", "2"]:
        encrypt() if choice == "1" else decrypt() 
        choice = input("ВАШ ВИБІР: ")

loop()