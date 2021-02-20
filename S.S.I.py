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
    amount = sum(countLetters.values())
    for letter, count in countLetters.items():
        OutputText.insert(END, "| " + letter + " | - " + str(count*100/sum(countLetters.values())) + "%\n")

def sorting():
    data = re.findall(r".+\s([a-zA-Zа-яїєіф])\D+(\d+.\d+)", OutputText.get("1.0", END))
    OutputText.delete("1.0", END)
    if RadioSortDirection.get() == 1:
        if RadioSort.get() == "period":
            sort = sorted(data, key = lambda x: float(x[1]))
            for letter, count in sort:
                OutputText.insert(END, "\t"*3 + "| " + letter + " | - " + str(count) + "%\n")
        else:
            sort = sorted(data, key = lambda x: x[0])
            for letter, count in sort:
                OutputText.insert(END, "\t"*3 + "| " + letter + " | - " + str(count) + "%\n")
    else:
        if RadioSort.get() == "period":
            sort = sorted(data, key = lambda x: float(x[1]), reverse=True)
            for letter, count in sort:
                OutputText.insert(END, "\t"*3 + "| " + letter + " | - " + str(count) + "%\n")
        else:
            sort = sorted(data, key = lambda x: x[0], reverse=True)
            for letter, count in sort:
                OutputText.insert(END, "\t"*3 + "| " + letter + " | - " + str(count) + "%\n")

def average(list1, n1, list2, n2, letter):
    p1, p2 = 0, 0
    # буква в одному слові але не в іншому або навпаки після двох слів
    #  program  file       program  file
    for tupl1, tupl2 in zip(list1, list2):
        if tupl1[0] == letter:
            p1 = tupl1[1]
        if tupl2[0] == letter:
            p2 = tupl2[1]
    if p1 == 0:
        print(letter)
    if p2 == 0:
        print(letter)
    return str((float(p1)*n1 + float(p2)*n2) / (n1 + n2))
    

def save():
    global isEmpty
    # якщо перший раз відкритий файл
    if not isEmpty:
        isEmpty += 1
        with open("Result.txt", "w") as file:
            for line in OutputText.get("1.0", END):
                file.write(line.encode('utf8').decode('cp1251'))
            file.write(f"Count of symbols: {amount}")
    # якщо другий раз
    else:
        with open("Result.txt", "r") as file:
            # усі букви і ймовірності в програмі(Список кортежів)
            inProgramTuples = re.findall(r".*\s([a-zA-Zа-яїєіф])\D+(\d+.\d+)%", OutputText.get("1.0", END))
            file.seek(0)
            # усі букви і ймовірності у файлі(Список кортежів)
            inFileTuples = re.findall(r".*\s([a-zA-Zа-яїєіф])\D+(\d+.\d+)%", file.read().encode('cp1251').decode('utf8'))
            file.seek(0)
            # кількість усіх букві у програмі
            ProgramSize = amount
            # кількість усіх букві у файлі
            FileSize = int(re.findall(r".*:\D+(\d+)", file.read())[0])
        # write new data in the file
        with open("Result.txt", "w") as file:
            allLetters = [x[0] for x in inProgramTuples] + [x[0] for x in inFileTuples]
            print(allLetters)
            # (P1N1 + P2N2) / (N1 + N2)
            while allLetters:
                for letter in allLetters:
                    if allLetters.count(letter) == 1:
                        file.write(f"| {letter.encode('utf8').decode('cp1251')} | - " + average(inProgramTuples, ProgramSize, inFileTuples, FileSize, letter) + "%\n")
                        allLetters.remove(letter)
                    else:
                        file.write(f"| {letter.encode('utf8').decode('cp1251')} | - " + average(inProgramTuples, ProgramSize, inFileTuples, FileSize, letter) + "%\n")
                        allLetters.remove(letter)
                        allLetters.remove(letter)
            file.write("Count of symbols: " + str(ProgramSize + FileSize))
            # print(inProgramTuples)
            # print(inFileTuples)
            # print(ProgramSize)
            # print(FileSize)

def clear():
    FileText.delete("1.0", END)
    OutputText.delete("1.0", END)

isEmpty = 0
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