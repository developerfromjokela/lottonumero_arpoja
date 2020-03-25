#  Copyright (c) 2020 Developer From Jokela. All rights reserved.

import random
import xml.etree.cElementTree as ET
import tkinter
from tkinter import filedialog
import tkinter.messagebox
from tkinter import simpledialog
import pathlib
import json

# Määritä tähän minkä haluat suurimmaksi luvuksi
maxNum = 150

# Lajittele numerot suuruusjärjestykseen pienemmästä suurempaan (True tai False)
sortNums = True

# Näytetäänkö GUI käyttöliittymä vai ei
gui = True


def generateLotteryNumbers(rows, number_in_row):
    lotteries = []
    i = 0
    while i < rows:
        row = generateLotteryRow(number_in_row)
        if sortNums:
            row.sort()
        lotteries.append(row)
        i = i + 1
    return lotteries


def generateLotteryRow(number_count):
    return random.sample(range(1, maxNum), number_count)


def checkForNumber(number):
    if not number.isdecimal():
        alert("Syötetty arvo ei ole numero, tai sisältää muutakin kuin numeroita", -1)
    else:
        return int(number)


def checkForType(type):
    type = type.replace(".","")
    if not type == "json" and not type == "xml" and not type == "csv" and not type == "txt":
        alert("Tuntematon tiedostotyyppi", -1)
    elif type == "json":
        return 0
    elif type == "xml":
        return 1
    elif type == "txt":
        return 2


def writeArrayToFile(array, filename, type):
    file=open(filename, "w")
    if type == 0:
        file.write(json.dumps(array))
    if type == 2:
        arrAsText = ""
        index=0
        for item in array:
            arrAsText = arrAsText + (','.join(map(str,item)))
            if not len(array) == index + 1:
                arrAsText = arrAsText + "\n"
            index=index+1
        file.write(arrAsText)
    if type == 1:
        file.close()
        root = ET.Element("lottonumerot")
        for item in array:
            doc = ET.SubElement(root, "lottorivi")
            for num in item:
                ET.SubElement(doc, "lottonumero").text = str(num)
        tree = ET.ElementTree(root)
        tree.write(filename)


def alert(text, code):
    if not gui:
        print("HUOMAUTUS: "+text)
    else:
        tkinter.messagebox.showinfo(title="Huomautus", message=text)
    exit(code)

def getFileExtension(num):
    if num==0:
        return ".json"
    elif num==1:
        return ".xml"
    elif num==2:
        return ".txt"


if not gui:
    rowsCount = checkForNumber(input("Syötä haluamasi lottorivimäärä: \n"))
    itemsInRow = checkForNumber(input("Syötä haluamasi lottonumeromäärä: \n"))
    ftInput = input("Syötä haluamasi tiedostomuoto (json, xml tai txt): \n")
    file_type = checkForType(ftInput)
    filename = input("Syötä tiedoston nimi: \n")
    if filename is "":
        alert("Tiedoston nimi on tyhjä! ", -1)
    writeArrayToFile(generateLotteryNumbers(rowsCount, itemsInRow), filename+getFileExtension(file_type), file_type)
else:
    ROOT = tkinter.Tk()
    ROOT.withdraw()
    rowsCount = simpledialog.askinteger(title="Käyttäjäsyöttö", prompt="Syötä haluamasi lottorivimäärä")
    if rowsCount == None:
        alert("Et syöttänyt mitään", -1)
    itemsInRow = simpledialog.askinteger(title="Käyttäjäsyöttö", prompt="Syötä haluamasi lottonumeromäärä")
    if itemsInRow == None:
        alert("Et syöttänyt mitään", -1)
    save_text_as = filedialog.asksaveasfile(mode='w',
                                            filetypes=[("Tekstitiedosto", ".txt"), ("JSON tiedosto", ".json"),
                                                       ("XML tiedosto", ".xml")])
    if save_text_as is None:
        alert("Tiedostoa ei valittu", -1)
    writeArrayToFile(generateLotteryNumbers(rowsCount, itemsInRow), save_text_as.name, checkForType(pathlib.Path(save_text_as.name).suffix))
    alert("Tiedosto tallennettu!", 0)
