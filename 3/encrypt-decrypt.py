import random
import re
# власний алгоритм генерації ключів
def createMatrix(matrix, rowNumbers, columnNumbers, data):
    matrix.append([0] + columnNumbers)
    index = 0
    for i in range(len(rowNumbers)):
        # add number on the beginning of a row
        rowForAppend = [rowNumbers[i]]
        for _ in range(len(columnNumbers)):
            # through every symbol of data
            rowForAppend += data[index]
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
                if matrix[0][j+1] > matrix[0][j+2]:
                    for k in range(len(matrix)):
                        matrix[k][j+1], matrix[k][j+2] =  matrix[k][j+2], matrix[k][j+1]
                    else:
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


def encrypt(): 
    matrix = []
    data = input("Введiть стрiчку для шифрування: ")
    rows, columns = [int(i) for i in input("Введiть кiлькiсть рядкiв та стовпцiв: ").split()]
    while rows*columns != len(data):
        print("Неможливо створити матрицю з такими розмiрами")
        rows, columns = [int(i) for i in input("Введiть кiлькiсть рядкiв та стовпцiв: ").split()]
    with open("logfile.txt", "w") as file:
        file.write(f"Count of rows: {rows}\nCount of columns: {columns}\n")
    rowKey = [i + 1 for i in range(rows)]
    columnKey = [i + 1 for i in range(columns)]
    random.shuffle(rowKey)
    random.shuffle(columnKey)
    createMatrix(matrix, rowKey, columnKey, data)
    encryptedMatrix(matrix, rowKey, columnKey)
    print(f"Row key: {rowKey}\nColumn key: {columnKey}")
    

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
            print(matrix[i][j], end="")
    print()

        
def loop():
    print("-"*11 + "┐\n1. Ecnrypt |\n2. Decrypt |\n" + "-"*11 + "┘")
    choice = input("Your choice: ")
    while choice in ["1", "2"]:
        encrypt() if choice == "1" else decrypt() 
        choice = input("Your choice: ")

loop()