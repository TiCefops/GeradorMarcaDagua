import os
from tkinter import *
from tkinter import filedialog

import pandas as pd
from PyPDF2 import PdfFileReader, PdfFileWriter

from scripts.createFoldersOnInit import createFoldersOnInit

locale = os.path.abspath(os.getcwd())
window = Tk()
inputPdf = ""
inputCsv = locale + "/dados.csv"
status = "Aguardando"

createFoldersOnInit()


def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/videos",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.PDF*"),
                                                     ("all files",
                                                      "*.*")))
    global inputPdf
    inputPdf = filename
    # Change label contents
    label_file_explorer.configure(text="Arquivo Aberto: " + filename)


def browseCsv():
    filename = filedialog.askopenfilename(initialdir="/videos",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.csv*"),
                                                     ("all files",
                                                      "*.*")))
    global inputCsv
    inputCsv = filename
    # Change label contents
    label_file_explorerCSV.configure(text="Arquivo CSV: " + inputCsv)


def create_watermarker():
    global status
    dados = pd.read_csv(inputCsv)
    label_file_status.config(text=status)
    label_file_status.config(text="Iniciando")
    label_file_status.update()

    for i, cpf in enumerate(dados["cpf"]):
        status = "Gerando " + str(i) + " de " + str(dados["cpf"].__len__())
        update(index=i, lenght=dados["cpf"].__len__())

        label_file_status.config(text=status)
        localMarca = locale + '\marca/' + cpf + ".pdf"
        pdf_writer = PdfFileWriter()
        watermark = localMarca
        pdf_reader = PdfFileReader(inputPdf)
        watermark_obj = PdfFileReader(watermark)
        watermark_page = watermark_obj.getPage(0)

        outpout = cpf + " " + os.path.basename(inputPdf).split('.', 1)[0] + ".pdf"

        for page in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page)
            page.mergePage(watermark_page)
            pdf_writer.addPage(page)

        with open(locale + '\gerados/' + outpout, "wb") as out:
            print(outpout)
            pdf_writer.write(out)
            out.closed

    label_file_status.config(text="Status: Concluído")


def update(index, lenght):
    label_file_status.config(text="Gerando " + str(index + 1) + " de " + str(lenght))
    label_file_status.update()


def gerarPdf():
    create_watermarker()


window.title("Gerador Marca D'Água v2 ")

# Set window size
window.geometry("600x550")

# Set window background color
window.config(background="white")
bg = PhotoImage(file="assets/bg.png")

label1 = Label(window, image=bg)
label1.place(x=130, y=150)

label2 = Label(window, text="Escola  Almeida  Santos - Itaquera, TEL:2745-2390",fg="blue")
label2.place(x=190, y=520)

# Create a File Explorer label
label_file_explorer = Label(window,
                            text="Local PDF",
                            width=100, height=1,
                            fg="blue")
label_file_explorerCSV = Label(window,
                               text="CSV PADRÃO Carregado : " + inputCsv,
                               width=100, height=1,
                               fg="blue")

label_file_status = Label(window,
                          text="Status: Aguardando",
                          width=40, height=1,
                          bg="white",
                          fg="blue")

button_explore = Button(window,
                        text="Selecione o PDF",
                        command=browseFiles)

button_csv = Button(window,
                    text="Selecione o CSV",
                    command=browseCsv)
button_gerar = Button(window,
                      text="Gerar Pdf",
                      command=gerarPdf)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column=1, row=1)
label_file_explorerCSV.grid(column=1, row=2)
button_explore.grid(column=1, row=3)
button_csv.grid(column=1, row=5)
button_gerar.grid(column=1, row=6)
label_file_status.grid(column=1, row=7)

# Let the window wait for any events
window.mainloop()
