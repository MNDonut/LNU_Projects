from tkinter import *
import re
import tkinter.messagebox
import logging


def findFile():
    try:
        with open(f"{FileNameEntry.get()}.txt", "r") as file:
            for line in file:
                InputText.insert("1.0", line)
    except FileNotFoundError:
        tkinter.messagebox.showerror("Помилка", "Файл не знайдено!")

def table():
    global frequencyDict, etalon
    data = InputText.get("1.0", END)
    frequencyDict, etalon = dict(), dict()
    countsymbols = len(data)
    with open("EtalonEng.txt", "r") as file:
        for line in file:
            etalon[line.split()[0]] = line.split()[1]
    for letter in data:
        if letter.lower() in "abcdefghijklmnopqrstuvwxyz":
            frequencyDict[letter.lower()] = frequencyDict.get(letter.lower(), 0) + 1
    for key in frequencyDict.keys():
        frequencyDict[key] = round(frequencyDict.get(key, 0) * 100 / countsymbols, 2)
    frequencyDict = dict(sorted(frequencyDict.items(), key=lambda item: float(item[1])))
    etalon = dict(sorted(etalon.items(), key=lambda item: float(item[1])))
    for (freKey, freVal), (keyEtalon, valEtalon) in zip(frequencyDict.items(), etalon.items()):
        FrequencyText.insert(END, f"\t{freKey} - {freVal}\t ---->\t{keyEtalon} - {valEtalon}\n")


def decrypt():
    with open("app.log", "w") as file:
        pass
    DecryptedText.delete("1.0", END)
    generalDict = {prev: curr for prev, curr in zip(frequencyDict.keys(), etalon.keys())}
    data = InputText.get("1.0", END)
    decrypted = []

    for symbol in data:
        if symbol in generalDict:
            decrypted.append(generalDict[symbol])
        elif symbol.lower() in generalDict:
            decrypted.append(generalDict[symbol.lower()].upper())
        else:
            decrypted.append(symbol)

    DecryptedText.insert(END, "".join(decrypted))
   
def change(indexes = []):
    # data = DecryptedText.get("1.0", END)
    data = list(DecryptedText.get("1.0", END))
    first = FirstEntry.get()
    second = SecondEntry.get()
    for i in range(len(data)):
        if data[i] == first and i not in indexes:
            data[i] = second
            indexes.append(i)
        elif data[i].lower() == first and i not in indexes:
            data[i] = second.upper()
            indexes.append(i)
    # data = data.replace(first.lower(), second.lower()).replace(first.upper(), second.upper())
    DecryptedText.delete("1.0", END)
    DecryptedText.insert(END, "".join(data))
    FirstEntry.delete(0, END)
    SecondEntry.delete(0, END)
    logging.basicConfig(filename='app.log', filemode='a', level = logging.INFO, format = "%(message)s")
    logging.info(f"{first} -> {second}")

def clear():
    InputText.delete("1.0", END)
    FrequencyText.delete("1.0", END)
    DecryptedText.delete("1.0", END)
    FileNameEntry.delete(0, 'end')
    FirstEntry.delete(0, 'end')
    SecondEntry.delete(0, 'end')

frequencyDict, etalon = {}, {}

root = Tk()
root.title("Дешифрування")
root.resizable(False, False)
root.geometry("1120x650")

HeadFrame = Frame(root)
HeadFrame.grid(row = 0, column = 0, pady = (5,))
ButtonsFrame = Frame(root)
ButtonsFrame.grid(row = 0, column = 1, pady = (5,))
ChangeFrame = Frame(root)
ChangeFrame.grid(row = 0, column = 2, padx = (15,), pady = (5,))
TextFrame = Frame(root)
TextFrame.grid(row = 1, column = 0, columnspan = 200, pady = (5,))

FileNameEntry = Entry(HeadFrame, width = 25, borderwidth = 1, relief = "solid")
FileNameEntry.grid(row = 0, column = 0, padx = 10, sticky = "NS")

FindFileButton = Button(ButtonsFrame, text = "Знайти файл", width = 15, height = 2, command = findFile)
FindFileButton.grid(row = 0, column = 0, padx = 5)
FrequencyButton = Button(ButtonsFrame, text = "Створити таблицю", width = 15, height = 2, command = table)
FrequencyButton.grid(row = 0, column = 1, padx = 5)
DecryptButton = Button(ButtonsFrame, text = "Дешифрувати", width = 15, height = 2, command = decrypt)
DecryptButton.grid(row = 0, column = 2, padx = 5)
ClearButton = Button(ButtonsFrame, text = "Очистити", width = 15, height = 2, command = clear)
ClearButton.grid(row = 0, column = 3, padx = 5)

FirstLabel = Label(ChangeFrame, text = "Замінити цей символ")
FirstLabel.grid(row = 0, column = 1)
FirstEntry = Entry(ChangeFrame, borderwidth = 1, relief = "solid")
FirstEntry.grid(row = 1, column = 1)
SecondEntry = Entry(ChangeFrame, borderwidth = 1, relief = "solid")
SecondEntry.grid(row = 1, column = 2, padx = 10)
SecondLabel = Label(ChangeFrame, text = "На цей")
SecondLabel.grid(row = 0, column = 2, padx = 10)
ChangeButton = Button(ChangeFrame, text = "Замінити", width = 20, command = change)
ChangeButton.grid(row = 0, column = 3, rowspan = 2, sticky = "NS")

InputText = Text(TextFrame, width = 45, height = 36, borderwidth = 1, relief = "solid")
InputText.grid(row = 1, column = 0, padx = 5)
FrequencyText = Text(TextFrame, width = 45, height = 36, borderwidth = 1, relief = "solid")
FrequencyText.grid(row = 1, column = 1, padx = 5)
DecryptedText = Text(TextFrame, width = 45, height = 36, borderwidth = 1, relief = "solid")
DecryptedText.grid(row = 1, column = 2, padx = 5)

root.mainloop()