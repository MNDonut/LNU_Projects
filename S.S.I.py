from tkinter import *
import re
import tkinter.messagebox

# уточнювати дані в моїй табличці після збереження 
# та порівнювати з еталоною

def findFile():
    FileText.delete("1.0", END)
    try:
        fileName = FileNameEntry.get().split(".")[0]
        with open(f"{fileName}.txt", "r") as file:
            for line in file:
                FileText.insert(END, line.encode('cp1251').decode('utf8'))
    except FileNotFoundError:
        tkinter.messagebox.showerror("Помилка", "Файл не знайдено!")

def table():
    OutputText.delete("1.0", END)
    countLetters = dict()
    for char in FileText.get("1.0", END):
        if char.isalpha() and not char.isdigit():
            if RadioLang.get() == "ukr" and char.lower() in "ячсмитьбюфівапролджєйцукенгшщзхї":
                countLetters[char.lower()] = countLetters.get(char.lower(), 0) + 1
            elif RadioLang.get() == "en" and char.lower() in "zxcvbnmasdfghjklqwertyuiop":
                countLetters[char.lower()] = countLetters.get(char.lower(), 0) + 1
    global amount
    amount = len(FileText.get("1.0", END)) - 1
    for letter, count in countLetters.items():
        OutputText.insert(END, "| " + letter + " | - " + str(count*100/amount) + "%\n")

def sorting():
    data = re.findall(r".+\s([a-zA-Zа-яїєіф])\D+(\d+.\d+)", OutputText.get("1.0", END))
    OutputText.delete("1.0", END)
    if RadioSortDirection.get() == 1:
        if RadioSort.get() == "period":
            sort = sorted(data, key = lambda x: float(x[1]))
            for letter, count in sort:
                OutputText.insert(END, "| " + letter + " | - " + str(count) + "%\n")
        else:
            sort = sorted(data, key = lambda x: x[0])
            for letter, count in sort:
                OutputText.insert(END, "| " + letter + " | - " + str(count) + "%\n")
    else:
        if RadioSort.get() == "period":
            sort = sorted(data, key = lambda x: float(x[1]), reverse=True)
            for letter, count in sort:
                OutputText.insert(END, "| " + letter + " | - " + str(count) + "%\n")
        else:
            sort = sorted(data, key = lambda x: x[0], reverse=True)
            for letter, count in sort:
                OutputText.insert(END, "| " + letter + " | - " + str(count) + "%\n")
    
def save(dictionary = {}):
    # update - change value or add a new pair
    ProgramTuples = re.findall(r".*\s([a-zA-Zа-яїєіф])\D+(\d+.\d+)%", OutputText.get("1.0", END))
    # all program tuples in this dict
    ProgramDict = dict()
    for pair in ProgramTuples:
        ProgramDict[pair[0]] = float(pair[1])
    ProgramSize = amount
    FileSize = 0
    f = open("Result.txt", "r")
    if len(f.read()) != 0:
        f.seek(0)
        FileSize = int(re.findall(r".*:\D+(\d+)", f.read())[0])
    else:
        FileSize = 0
    #update prev
    for key, val in dictionary.items():
        if key in ProgramDict.keys():
            dictionary[key] = (ProgramDict[key] * ProgramSize + val * FileSize) / (ProgramSize + FileSize)
        # if key no in programdict => programdict[key] = 0
        else:
            dictionary[key] = (val * FileSize) / (ProgramSize + FileSize)

    #add unique(than it's not in file => val = 0)
    for pair in ProgramTuples:
        if pair[0] not in dictionary.keys():
            dictionary[pair[0]] = (float(pair[1]) * ProgramSize) / (FileSize + ProgramSize)

    f.close()
    f = open("Result.txt", "w")
    for key, val in dictionary.items():
        f.write("| " + key.encode('utf8').decode('cp1251') + " | - " + str(val) + "%\n")
    etalon = open("Etalon.txt", "r")
    etalondict = dict()
    for line in etalon:
        etalondict[line.split()[0].encode('cp1251').decode('utf8')] = float(line.split()[1])
    final = open("Final.txt", "w")
    final.write(("Максимальну частоту повторювань в еталоній таблиці має літера " + max(etalondict, key = lambda x: etalondict[x]) + " із значенням " + str(etalondict[max(etalondict, key = lambda x: etalondict[x])])).encode('utf8').decode('cp1251'))
    final.write(("\nУ нашій же таблиці максимальну частоту повторень має літера " + max(dictionary, key = lambda x: dictionary[x]) + " із значенням " + str(dictionary[max(dictionary, key = lambda x: dictionary[x])])).encode('utf8').decode('cp1251'))
    final.write(("\nМінімальну частоту повторювань в еталоній таблиці має літера " + min(etalondict, key = lambda x: etalondict[x]) + " із значенням " + str(etalondict[min(etalondict, key = lambda x: etalondict[x])])).encode('utf8').decode('cp1251'))
    final.write(("\nУ нашій же таблиці мінімальну частоту повторень має літера " + min(dictionary, key = lambda x: dictionary[x]) + " із значенням " + str(dictionary[min(dictionary, key = lambda x: dictionary[x])])).encode('utf8').decode('cp1251'))
    f.write("\nКількість символів: ".encode('utf8').decode('cp1251') + str(ProgramSize + FileSize))
    f.close()
    etalon.close()
    final.close()


def clear():
    FileText.delete("1.0", END)
    OutputText.delete("1.0", END)

amount = 0

root = Tk()
root.title("Частотний Аналіз")
root.resizable(False, False)
root.geometry("1350x730")

HeadFrame = Frame(root, width = 1350, height = 730)
HeadFrame.grid(row = 0, column = 0)
RadioFrame = Frame(HeadFrame, width = 450, height = 50)
RadioFrame.grid(row = 0, column = 0)
EntryFrame = Frame(HeadFrame, width = 450, height = 50)
EntryFrame.grid(row = 0, column = 1)
ButtonFrame = Frame(HeadFrame, width = 450, height = 50)
ButtonFrame.grid(row = 0, column = 2)
TextFrame = Frame(root, width = 1350, height = 690)
TextFrame.grid(row = 1, column = 0, columnspan = 2)

RadioLang = StringVar()
RadioLang.set("ukr")
ukr = Radiobutton(RadioFrame, font=("TimesNewRoman", 14), text = "Українська", value = "ukr", variable = RadioLang)
ukr.grid(row = 0, column = 0, rowspan = 2)
en = Radiobutton(RadioFrame, font=("TimesNewRoman", 14), text = "Англійська", value = "en", variable = RadioLang)
en.grid(row = 0, column = 1, rowspan = 2)

RadioSort = StringVar()
RadioSort.set("period")
alpha = Radiobutton(RadioFrame, font=("TimesNewRoman", 14), text = "За частотою", value = "period", variable = RadioSort)
alpha.grid(row = 0, column = 2, sticky = "W", pady=(5, 0))
period = Radiobutton(RadioFrame, font=("TimesNewRoman", 14), text = "За алфавітом", value = "alpha", variable = RadioSort)
period.grid(row = 0, column = 3, sticky = "EW", pady=(5, 0))

RadioSortDirection = BooleanVar()
up = Radiobutton(RadioFrame, font=("TimesNewRoman", 14), text = "Зростання", value = 1, variable = RadioSortDirection)
up.grid(row = 1, column = 2, sticky = "W")
down = Radiobutton(RadioFrame, font=("TimesNewRoman", 14), text = "Спадання", value = 0, variable = RadioSortDirection)
down.grid(row = 1, column = 3, sticky = "W")

FileNameEntry = Entry(EntryFrame, width = 40)
FileNameEntry.grid(row = 0, pady = (5, 2), padx = (10,))
FileNameButton = Button(EntryFrame, text = "Знайти файл", command = findFile)
FileNameButton.grid(row = 1, sticky = "EW", padx = (10,))

CreateButton = Button(ButtonFrame, text = "Створити таблицю", width = 18, height = 2, command = table)
CreateButton.grid(row = 0, column = 0)
SortButton = Button(ButtonFrame, text = "Сортувати", width = 18, height = 2, command = sorting)
SortButton.grid(row = 0, column = 1)
SaveButton = Button(ButtonFrame, text = "Зберегти", width = 18, height = 2, command = save)
SaveButton.grid(row = 0, column = 2)
ClearButton = Button(ButtonFrame, text = "Очистити", width = 18, height = 2, command = clear)
ClearButton.grid(row = 0, column = 3)

FileText = Text(TextFrame, borderwidth = 2, relief = "solid", height = 38)
FileText.grid(row = 0, column = 0, sticky = "NS", pady = (20, 0), padx = (0, 10))
OutputText = Text(TextFrame, borderwidth = 2, relief = "solid", height = 38)
OutputText.grid(row = 0, column = 1, sticky = "NS", pady = (20, 0), padx = (10, 0))

root.mainloop()