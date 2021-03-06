import random
import re

def createMatrix(matrix, rowNumbers, columnNumbers, data):
    matrix.append([0] + columnNumbers)
    # data len = 31
    # 5 7
    index = 0
    for i in range(len(rowNumbers)):
        # add number on the beginning of a row
        rowForAppend = [rowNumbers[i]]
        for _ in range(len(columnNumbers)):
            # through every symbol of data
            if index < len(data):
                rowForAppend += data[index]
                index += 1
            else:
                rowForAppend += "$"
                index += 1
        matrix.append(rowForAppend)
        
        
    print("-"*15 + "\nСтрічка у вигляді матриці:")
    for row in matrix:
        print(" ".join(str(x) for x in row))
    print("-"*15)

def encryptedMatrix(matrix, rowKey, columnKey):
    print("Посортована матриця за стовпцями:")
    with open("logfile.txt", "a") as file:
        for i in range(len(columnKey)):
            for j in range(len(columnKey) - i - 1):
                # not j because of first zero
                if matrix[0][j+1] > matrix[0][j+2]:
                    for k in range(len(matrix)):
                        matrix[k][j+1], matrix[k][j+2] =  matrix[k][j+2], matrix[k][j+1]
                    else:
                        # if j then j+1 column
                        file.write(f"Change {j+2} column with {j+3} column\n")

        for row in matrix:
            print(" ".join(str(x) for x in row))
        print("-"*15)
        # logging
        copyRowKey = rowKey.copy()
        for i in range(len(rowKey)):
            for j in range(len(rowKey) - i - 1):
                if copyRowKey[j] > copyRowKey[j+1]:
                    copyRowKey[j], copyRowKey[j+1] = copyRowKey[j+1], copyRowKey[j]
                    file.write(f"Change {j+2} row with {j+3} row\n")

    matrix = sorted(matrix, key = lambda x: x[0])

    print("Посортована матриця за рядками:")
    for row in matrix:
        print(" ".join(str(x) for x in row))

    print("-"*15)
        
    with open("encrypt.txt", "w+") as file:
        file.write("Row key: " + " ".join(str(x) for x in rowKey) + "\n")
        file.write("Column key: " + " ".join(str(x) for x in columnKey) + "\n")
        for i in range(1, len(rowKey) + 1):
            for j in range(1, len(columnKey) + 1):
                file.write(str(f"{matrix[i][j]}").encode('utf8').decode('cp1251'))

def shuffle(keys):
    for i in range(len(keys) - 1, 0, -1):
        j = random.randint(0, i)
        keys[j], keys[i] = keys[i], keys[j]

def encrypt(): 
    matrix = []
    data = input("Введiть стрiчку для шифрування: ")
    print(f"Довжина стрічки: {len(data)}")
    rows, columns = [int(i) for i in input("Введiть кiлькiсть рядкiв та стовпцiв: ").split()]
    # while rows*columns != len(data):
    #     print("Неможливо створити матрицю з такими розмiрами")
    #     rows, columns = [int(i) for i in input("Введiть кiлькiсть рядкiв та стовпцiв: ").split()]
    with open("logfile.txt", "w") as file:
        file.write(f"Count of rows: {rows}\nCount of columns: {columns}\n")
    rowKey = [i + 1 for i in range(rows)]
    columnKey = [i + 1 for i in range(columns)]
    shuffle(rowKey)
    shuffle(columnKey)
    print(f"ROW KEY: {rowKey}\nCOLUMN KEY: {columnKey}")
    createMatrix(matrix, rowKey, columnKey, data)
    encryptedMatrix(matrix, rowKey, columnKey)
    

def decrypt():
    with open("encrypt.txt", "r") as file:
        rowKey, columnKey = re.findall(r"(?:\d+\s*)+\d+", file.read())
        rowKey = [int(i) for i in rowKey.split()]
        columnKey = [int(i) for i in columnKey.split()]
        file.seek(0)
        data = file.readlines()[-1].encode('cp1251').decode('utf8')

    print(f"Зашифрований текст: {data}")
    matrix = []
    matrix.append([0] + columnKey)
    index = 0
    for i in range(len(rowKey)):
        rowForAppend = [rowKey[i]]
        for _ in range(len(columnKey)):
            rowForAppend += data[index]
            index += 1
        matrix.append(rowForAppend)

    for row in matrix:
        print(" ".join(str(x) for x in row))
    print("-"*15 + "\nРозшифрований текст: ", end = "")
    # decrypting
    for i in rowKey:
        for j in columnKey:
            if matrix[i][j] == "$":
                continue
            print(matrix[i][j], end="")
    print()

        
def loop():
    print("-"*16 + "┐\n1. Зашифрувати  |\n2. Розшифрувати |\n" + "-"*16 + "┘")
    choice = input("ВАШ ВИБІР: ")
    while choice in ["1", "2"]:
        encrypt() if choice == "1" else decrypt() 
        choice = input("ВАШ ВИБІР: ")

loop()