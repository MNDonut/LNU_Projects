import random

UKR = [['а', 'б', 'в', 'г', 'д', 'е'],
       ['є', 'ж', 'з', 'и', 'і', 'к'],
       ['л', 'м', 'н', 'о', 'п', 'р'],
       ['с', 'т', 'у', 'ф', 'х', 'ц'],
       ['ч', 'ш', 'щ', 'ь', 'ю', 'я'],
       ['ґ', 'й', 'ї', 'ґ', 'й', 'ї']]

EN = [["a", "b", "c", "d", "e"],
      ["f", "g", "h", "i", "k"],
      ["l", "m", "n", "o", "p"],
      ["q", "r", "s", "t", "u"],
      ["v", "w", "x", "y", "z"]]

def shuffle(matrix):
    for i in range(len(matrix) - 1, 0, -1):
        for j in range(len(matrix[i])):
            randCol = random.randint(0, i)
            matrix[i][j], matrix[randCol][j] = matrix[randCol][j], matrix[i][j]
    for i in range(len(matrix)):
        for j in range(len(matrix[i]) - 1, 0, -1):
            randRow = random.randint(0, i)
            matrix[i][j], matrix[i][randRow] = matrix[i][randRow], matrix[i][j]
    for row in matrix:
        print(row)
    return matrix

def encrypt():
    language = input("Виберіть мову: (ukr) або (en) - ").lower()
    currentMatrix = shuffle(UKR) if language == "ukr" else shuffle(EN)
    phrase = input("Введiть фразу для шифрування: ")
    columnRowPairs = list()
    spaceIndexes = [i for i in range(len(phrase)) if phrase[i] == " "]
    for letter in phrase:
        for i in range(len(currentMatrix)):
            for j in range(len(currentMatrix[i])):
                if currentMatrix[i][j] == letter.lower():
                    # number of column and row, not indexes
                    columnRowPairs.append((j+1, i+1))

    for letter in "".join(phrase.split()):
        print(letter, end=" ")
    print()
    for one in columnRowPairs:
        print(str(one[0]), end=" ")
    print()
    for two in columnRowPairs:
        print(str(two[1]), end=" ")
    print()
    groupedIndexes = ["".join(["".join(str(two)) for two in pair]) for pair in columnRowPairs]
    groupedIndexes = [x[0] for x in groupedIndexes] + [x[1] for x in groupedIndexes]
    encryptedText = ""
    for i in range(0, int(len(groupedIndexes)), 2):
        encryptedText += currentMatrix[int(groupedIndexes[i+1])-1][int(groupedIndexes[i])-1]
    encryptedText = list(encryptedText)
    for i in spaceIndexes:
        encryptedText.insert(i, "#")
    encryptedText = "".join(encryptedText)
    print(f"Encrypted text: {encryptedText}")
    with open("keys.txt", "w") as file:
        if language == "en":
            file.write("Encrypted text: " + encryptedText)
        else:
            file.write("Encrypted text: " + encryptedText.encode('utf8').decode('cp1251'))
        file.write("\nKeys: ")
        for i in range(0, len(groupedIndexes), 2):
            file.write(groupedIndexes[i] + groupedIndexes[i+1] + " ")

    with open("matrix.txt", "w") as file:
        for row in currentMatrix:
            file.write(" ".join(str(x) for x in row).encode('utf8').decode('cp1251') + "\n")
    

def decrypt():
    matrix = []
    with open("matrix.txt", "r") as file:
        for line in file:
            matrix.append([i.encode('cp1251').decode('utf8') for i in line.split()])
    with open("keys.txt", "r") as file:
        text = file.readline().split(": ")[1].encode('cp1251').decode('utf8')
        indexes = "".join((file.readline().split(": ")[1]).split())
    spaceIndexes = [i for i in range(len(text)) if text[i] == "#"]
    result = []
    for i in range(len(indexes)//2):
        result.append(matrix[int(indexes[int(len(indexes)//2 + i)]) - 1][int(indexes[i]) - 1])
    for i in spaceIndexes:
        result.insert(i, " ")
    print("".join(result))
        

def loop():
    print("-"*16 + "┐\n1. Зашифрувати  |\n2. Розшифрувати |\n" + "-"*16 + "┘")
    choice = input("ВАШ ВИБІР: ")
    while choice in ["1", "2"]:
        encrypt() if choice == "1" else decrypt() 
        choice = input("ВАШ ВИБІР: ")

loop()