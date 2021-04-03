# coding = utf-8

import os
import pickle
import tkinter as tk
from tkinter import *
from tkinter import ttk, simpledialog, messagebox
from mbox import MessageBox

import fpdf
import pdf2image
from PIL import Image, ImageTk
from fpdf import FPDF

fpdf.set_global("SYSTEM_TTFONTS", 'fonts')
data = []


def mbox(msg, b1, b2, b3, frame=True, t=False, entry=False):
    msgbox = MessageBox(msg, b1, b2, b3, frame, t, entry)
    msgbox.root.mainloop()
    # the function pauses here until the mainloop is quit
    msgbox.root.destroy()
    return msgbox.returning


def loadpresets():
    with open('data_folder/sabloni.txt', 'rb') as f:
        try:
            data = pickle.load(open("data_folder/sabloni.txt", "rb"))
        except EOFError:
            data = []
        for dictionary in data:
            sabloniListbox.insert(END, dictionary['preset_name'])


def exporter(export_name):
    if export_name != "" and export_name not in sabloniListbox.get(0, END):
        with open('data_folder/sabloni.txt', 'rb') as f:
            try:
                data = pickle.load(open("data_folder/sabloni.txt", "rb"))
            except EOFError:
                data = []
        with open('data_folder/sabloni.txt', 'wb') as f:
            dict1 = {'preset_name': export_name}
            data.append(dict1)

            for keyword in kwords:
                exec(f"dict1['{keyword}'] = {keyword}Menu.get()")
            pickle.dump(data, f)
            sabloniListbox.insert(END, export_name)
    else:

        if export_name == "":
            messagebox.showerror("GREŠKA", "IME ŠABLONA NIJE UNETO!")
        else:
            response = mbox('ŠABLON SA IMENOM ' + export_name + ' VEĆ POSTOJI!\n\nODABERITE AKCIJU:', 'PRESNIMI',
                            'PREIMENUJ', 'ODUSTANI')
            if response == "overwrite":

                with open('data_folder/sabloni.txt', 'rb') as f:
                    try:
                        data = pickle.load(open("data_folder/sabloni.txt", "rb"))
                        for dictionary in data:
                            if dictionary['preset_name'] == export_name:
                                dict1 = dictionary
                    except EOFERROR:
                        data = []

                with open('data_folder/sabloni.txt', 'wb') as f:

                    for keyword in kwords:
                        exec(f"dict1['{keyword}'] = {keyword}Menu.get()")
                    pickle.dump(data, f)
            elif response == "rename":
                exportUnos.delete(0, END)
            else:
                pass


def importer():
    if sabloniListbox.curselection():
        with open('data_folder/sabloni.txt', 'rb') as f:
            data = pickle.load(f)
            for dictionary in data:
                if dictionary['preset_name'] == sabloniListbox.get(ACTIVE):
                    selected_dict = dictionary
                    break

        for keyword in kwords:
            form_preview(f'{keyword}', selected_dict.get(keyword))
    else:
        pass


def delete_preset():
    try:
        selected = sabloniListbox.curselection()[0]
        sabloniListbox.delete(selected)
        with open("data_folder/sabloni.txt", 'rb') as f:
            lines = pickle.load(f)
            del lines[selected]
        with open("data_folder/sabloni.txt", 'wb') as f:
            pickle.dump(lines, f)
    except IndexError:
        pass


def printer():
    os.startfile('labels.pdf')


def popup_add(menu, location):
    answer = simpledialog.askstring("Input", "Unesi novu vrednost: ", parent=master)
    if answer not in menu['values'] and answer is not None:
        menu['values'] = (*menu['values'], answer)
        with open(f"data_folder/{location}", 'a+', encoding='utf8') as f:
            f.write(answer + '\n')
    else:
        messagebox.showerror("Error", "Ova vrednost već postoji!")


def delete(menu, selected, location):
    temp = list(menu['values'])
    try:
        temp.remove(selected)
    except ValueError:
        pass
    menu['values'] = tuple(temp)
    with open(f"data_folder/{location}", "r", encoding='utf-8') as f:
        lines = f.readlines()
    with open(f"data_folder/{location}", "w", encoding='utf-8') as f:
        for line in lines:
            if line.strip("\n") != selected:
                f.write(line)
    try:
        menu.current(len(menu['values']) - 1)
    except TclError:
        menu.current()

preview_data = {'poreklo': '', 'uvoznik': '', 'proizvodjac': '', 'uverenje': '', 'naziv': '',
                'artikal': '', 'lice': '', 'postava': '', 'djon': '', 'srps': '', 'izrada': '',
                'namena': '', 'odrzavanje': ''}


def form_preview(box, box_value):
    preview_data[box] = box_value
    pdf1 = FPDF('L', 'mm', (37.1, 70))
    pdf1.add_font("NotoSans", style="", fname="NotoSans-Regular.ttf", uni=True)
    pdf1.add_font("NotoSansBold", style="", fname="NotoSans-Bold.ttf", uni=True)
    pdf1.set_font("NotoSans", size=12)
    pdf1.set_auto_page_break(0)
    pdf1.set_margins(2, 2.8, 4)
    pdf1.add_page()
    columnsize = 70

    data = f"""ZEMLJA POREKLA: {preview_data['poreklo']}
UVOZNIK: {preview_data['uvoznik']}
PROIZVOĐAČ: {preview_data['proizvodjac']}
UVERENJE BR: {preview_data['uverenje']}
NAZIV ROBE: {preview_data['naziv']}
ARTIKAL: {preview_data['artikal']}
SIROVINSKI SASTAV: LICE-{preview_data['lice']}, POSTAVA-{preview_data['postava']}
                                      ĐON-{preview_data['djon']}
SRPS: {preview_data['srps']}
NAČIN IZRADE: {preview_data['izrada']}
NAMENA: {preview_data['namena']}
ODRŽAVANJE: {preview_data['odrzavanje']}
"""
    text = "D E K L A R A C I J A     "
    pdf1.set_font('NotoSansBold', '', 8)
    pdf1.cell(columnsize, 1.2, text, align="C")
    pdf1.ln()
    pdf1.cell(columnsize, 1, "")
    pdf1.ln()
    for line in data.splitlines():
        text = line
        pdf1.set_font('NotoSans', '', 5)
        pdf1.cell(columnsize, 2, text, align="L")
        pdf1.ln()

    pdf1.cell(columnsize, 1.6, "")
    pdf1.ln()
    text = "KVALITET KONTROLISAO JUGOINSPEKT BEOGRAD       "
    pdf1.set_font('NotoSansBold', '', 6)
    pdf1.cell(columnsize, 0, text, align="C")
    pdf1.ln()
    pdf1.cell(columnsize, 6.6, "")
    pdf1.ln()

    pdf1.output('preview.pdf', 'F')
    preview = pdf2image.convert_from_path(poppler_path='POPPLER/poppler-21.02.0/Library/bin',
                                          pdf_path='preview.pdf', dpi=300)
    preview[0].save('out.jpg', 'JPEG')

    generate_preview()


def generate_preview():
    load = Image.open('out.jpg')
    resized_load = load.resize((round(load.size[0] * 0.5), round(load.size[1] * 0.5)))
    render = ImageTk.PhotoImage(resized_load)

    img = Label(image=render)
    img.image = render
    img.place(relx=0.5, rely=0.5, anchor=CENTER)

    form_pdf()


def form_pdf():
    pdf = FPDF(unit='mm', format='A4')
    # define one column and one row margins

    pdf.set_auto_page_break(0)
    pdf.set_margins(2, 2.8, 4)
    pdf.add_font("NotoSans", style="", fname="NotoSans-Regular.ttf", uni=True)
    pdf.add_font("NotoSansBold", style="", fname="NotoSans-Bold.ttf", uni=True)
    pdf.set_font("NotoSans", size=12)

    pdf.add_page()
    # define total rows containing labels
    rows = 8
    # define total columns containing labels
    cols = 3
    columnsize = 70

    data = f"""    ZEMLJA POREKLA: {preview_data['poreklo']}
    UVOZNIK: {preview_data['uvoznik']}
    PROIZVOĐAČ: {preview_data['proizvodjac']}
    UVERENJE BR: {preview_data['uverenje']}
    NAZIV ROBE: {preview_data['naziv']}
    ARTIKAL: {preview_data['artikal']}
    SIROVINSKI SASTAV: LICE-{preview_data['lice']}, POSTAVA-{preview_data['postava']}
                                          ĐON-{preview_data['djon']}
    SRPS: {preview_data['srps']}
    NAČIN IZRADE: {preview_data['izrada']}
    NAMENA: {preview_data['namena']}
    ODRŽAVANJE: {preview_data['odrzavanje']}
    """

    for i in range(rows):
        pdf.cell(columnsize, 2, "")
        pdf.ln()
        for j in range(cols):
            text = "D E K L A R A C I J A"
            pdf.set_font('NotoSansBold', '', 8)
            pdf.cell(columnsize, 1.2, text, align="C")
        pdf.ln()
        pdf.cell(columnsize, 1, "")
        pdf.ln()
        for line in data.splitlines():
            for j in range(cols):
                text = line
                pdf.set_font('NotoSans', '', 5)
                pdf.cell(columnsize, 2, text, align="L")
            pdf.ln()

        # pdf.cell(columnsize, 0.1, "")
        # pdf.ln()
        for j in range(cols):
            text = "KVALITET KONTROLISAO JUGOINSPEKT BEOGRAD"
            pdf.set_font('NotoSansBold', '', 6)
            pdf.cell(columnsize, 0, text, align="C")
        pdf.ln()
        pdf.cell(columnsize, 6.9, "")
        pdf.ln()

    pdf.output('labels.pdf', 'F')


kwords = ['poreklo', 'uvoznik', 'proizvodjac', 'uverenje', 'naziv', 'artikal', 'lice',
          'postava', 'djon', 'srps', 'izrada', 'namena', 'odrzavanje']

for keyword in kwords:
    with open(f'data_folder/{keyword}.txt', encoding='utf-8', errors='ignore') as f:
        exec(f'{keyword}Values = [line.strip() for line in f]')


def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))


master = tk.Tk()
master.title("DEKLARACIJE")
master.minsize(width=1105, height=600)
master.maxsize(width=1105, height=600)

canvas = Canvas(master)
canvas.place(relx=0, rely=0, relheight=1, relwidth=1)
frame = Frame(master)
frame.bind('<Configure>', on_configure)
canvas.create_window(0, 0, window=frame)

porekloDelete = Button(master, text="OBRIŠI", command=lambda: delete(porekloMenu, porekloMenu.get(), 'poreklo.txt'))
porekloDelete.grid(column=0, row=5, padx=10, pady=10)
poreklo = tk.StringVar()
porekloMenu = ttk.Combobox(master, width=27, textvariable=poreklo, state="readonly")
porekloMenu['values'] = porekloValues
porekloMenu.grid(column=1, row=5, pady=10)
porekloMenu.set('Poreklo')
porekloAdd = Button(master, text="DODAJ", command=lambda: popup_add(porekloMenu, 'poreklo.txt'))
porekloAdd.grid(column=2, row=5, padx=10, pady=10)
porekloMenu.current()

uvoznikDelete = Button(master, text="OBRIŠI", command=lambda: delete(uvoznikMenu, uvoznikMenu.get(), 'uvoznik.txt'))
uvoznikDelete.grid(column=0, row=6, padx=10, pady=10)
uvoznik = tk.StringVar()
uvoznikMenu = ttk.Combobox(master, width=27, textvariable=uvoznik, state="readonly")
uvoznikMenu['values'] = uvoznikValues
uvoznikMenu.grid(column=1, row=6, pady=10)
uvoznikMenu.set('Uvoznik')
uvoznikAdd = Button(master, text="DODAJ", command=lambda: popup_add(uvoznikMenu, 'uvoznik.txt'))
uvoznikAdd.grid(column=2, row=6, padx=10, pady=10)
uvoznikMenu.current()

proizvodjacDelete = Button(master, text="OBRIŠI",
                           command=lambda: delete(proizvodjacMenu, proizvodjacMenu.get(), 'proizvodjac.txt'))
proizvodjacDelete.grid(column=0, row=7, padx=10, pady=10)
proizvodjac = tk.StringVar()
proizvodjacMenu = ttk.Combobox(master, width=27, textvariable=proizvodjac, state="readonly")
proizvodjacMenu['values'] = proizvodjacValues
proizvodjacMenu.grid(column=1, row=7, pady=10)
proizvodjacMenu.set('Proizvođač')
proizvodjacAdd = Button(master, text="DODAJ", command=lambda: popup_add(proizvodjacMenu, 'proizvodjac.txt'))
proizvodjacAdd.grid(column=2, row=7, padx=10, pady=10)
proizvodjacMenu.current()

uverenjeDelete = Button(master, text="OBRIŠI", command=lambda: delete(uverenjeMenu, uverenjeMenu.get(), 'uverenje.txt'))
uverenjeDelete.grid(column=0, row=8, padx=10, pady=10)
uverenje = tk.StringVar()
uverenjeMenu = ttk.Combobox(master, width=27, textvariable=uverenje, state="readonly")
uverenjeMenu['values'] = uverenjeValues
uverenjeMenu.grid(column=1, row=8, pady=10)
uverenjeMenu.set('Uverenje')
uverenjeAdd = Button(master, text="DODAJ", command=lambda: popup_add(uverenjeMenu, 'uverenje.txt'))
uverenjeAdd.grid(column=2, row=8, padx=10, pady=10)
uverenjeMenu.current()

nazivDelete = Button(master, text="OBRIŠI", command=lambda: delete(nazivMenu, nazivMenu.get(), 'naziv.txt'))
nazivDelete.grid(column=0, row=9, padx=10, pady=10)
naziv = tk.StringVar()
nazivMenu = ttk.Combobox(master, width=27, textvariable=naziv, state="readonly")
nazivMenu['values'] = nazivValues
nazivMenu.grid(column=1, row=9, pady=10)
nazivMenu.set('Naziv')
nazivAdd = Button(master, text="DODAJ", command=lambda: popup_add(nazivMenu, 'naziv.txt'))
nazivAdd.grid(column=2, row=9, padx=10, pady=10)
nazivMenu.current()

artikalDelete = Button(master, text="OBRIŠI", command=lambda: delete(artikalMenu, artikalMenu.get(), 'artikal.txt'))
artikalDelete.grid(column=0, row=10, padx=10, pady=10)
artikal = tk.StringVar()
artikalMenu = ttk.Combobox(master, width=27, textvariable=artikal, state="readonly")
artikalMenu['values'] = artikalValues
artikalMenu.grid(column=1, row=10, pady=10)
artikalMenu.set('Artikal')
artikalAdd = Button(master, text="DODAJ", command=lambda: popup_add(artikalMenu, 'artikal.txt'))
artikalAdd.grid(column=2, row=10, padx=10, pady=10)
artikalMenu.current()

liceDelete = Button(master, text="OBRIŠI", command=lambda: delete(liceMenu, liceMenu.get(), 'lice.txt'))
liceDelete.grid(column=0, row=11, padx=10, pady=10)
lice = tk.StringVar()
liceMenu = ttk.Combobox(master, width=27, textvariable=lice, state="readonly")
liceMenu['values'] = liceValues
liceMenu.grid(column=1, row=11, pady=10)
liceMenu.set('Lice')
liceAdd = Button(master, text="DODAJ", command=lambda: popup_add(liceMenu, 'lice.txt'))
liceAdd.grid(column=2, row=11, padx=10, pady=10)
liceMenu.current()

postavaDelete = Button(master, text="OBRIŠI", command=lambda: delete(postavaMenu, postavaMenu.get(), 'postava.txt'))
postavaDelete.grid(column=0, row=12, padx=10, pady=10)
postava = tk.StringVar()
postavaMenu = ttk.Combobox(master, width=27, textvariable=postava, state="readonly")
postavaMenu['values'] = postavaValues
postavaMenu.grid(column=1, row=12, pady=10)
postavaMenu.set('Postava')
postavaAdd = Button(master, text="DODAJ", command=lambda: popup_add(postavaMenu, 'postava.txt'))
postavaAdd.grid(column=2, row=12, padx=10, pady=10)
postavaMenu.current()

djonDelete = Button(master, text="OBRIŠI", command=lambda: delete(djonMenu, djonMenu.get(), 'djon.txt'))
djonDelete.grid(column=0, row=13, padx=10, pady=10)
djon = tk.StringVar()
djonMenu = ttk.Combobox(master, width=27, textvariable=djon, state="readonly")
djonMenu['values'] = djonValues
djonMenu.grid(column=1, row=13, pady=10)
djonMenu.set('Đon')
djonAdd = Button(master, text="DODAJ", command=lambda: popup_add(djonMenu, 'djon.txt'))
djonAdd.grid(column=2, row=13, padx=10, pady=10)
djonMenu.current()

srpsDelete = Button(master, text="OBRIŠI", command=lambda: delete(srpsMenu, srpsMenu.get(), 'srps.txt'))
srpsDelete.grid(column=0, row=14, padx=10, pady=10)
srps = tk.StringVar()
srpsMenu = ttk.Combobox(master, width=27, textvariable=srps, state="readonly")
srpsMenu['values'] = srpsValues
srpsMenu.grid(column=1, row=14, pady=10)
srpsMenu.set('SRPS')
srpsAdd = Button(master, text="DODAJ", command=lambda: popup_add(srpsMenu, 'srps.txt'))
srpsAdd.grid(column=2, row=14, padx=10, pady=10)
srpsMenu.current()

izradaDelete = Button(master, text="OBRIŠI", command=lambda: delete(izradaMenu, izradaMenu.get(), 'izrada.txt'))
izradaDelete.grid(column=0, row=15, padx=10, pady=10)
izrada = tk.StringVar()
izradaMenu = ttk.Combobox(master, width=27, textvariable=izrada, state="readonly")
izradaMenu['values'] = izradaValues
izradaMenu.grid(column=1, row=15, pady=10)
izradaMenu.set('Izrada')
izradaAdd = Button(master, text="DODAJ", command=lambda: popup_add(izradaMenu, 'izrada.txt'))
izradaAdd.grid(column=2, row=15, padx=10, pady=10)
izradaMenu.current()

namenaDelete = Button(master, text="OBRIŠI", command=lambda: delete(namenaMenu, namenaMenu.get(), 'namena.txt'))
namenaDelete.grid(column=0, row=16, padx=10, pady=10)
namena = tk.StringVar()
namenaMenu = ttk.Combobox(master, width=27, textvariable=namena, state="readonly")
namenaMenu['values'] = namenaValues
namenaMenu.grid(column=1, row=16, pady=10)
namenaMenu.set('Namena')
namenaAdd = Button(master, text="DODAJ", command=lambda: popup_add(namenaMenu, 'namena.txt'))
namenaAdd.grid(column=2, row=16, padx=10, pady=10)
namenaMenu.current()

odrzavanjeDelete = Button(master, text="OBRIŠI",
                          command=lambda: delete(odrzavanjeMenu, odrzavanjeMenu.get(), 'odrzavanje.txt'))
odrzavanjeDelete.grid(column=0, row=17, padx=10, pady=10)
odrzavanje = tk.StringVar()
odrzavanjeMenu = ttk.Combobox(master, width=27, textvariable=odrzavanje, state="readonly")
odrzavanjeMenu['values'] = odrzavanjeValues
odrzavanjeMenu.grid(column=1, row=17, pady=10)
odrzavanjeMenu.set('Održavanje')
odrzavanjeAdd = Button(master, text="DODAJ", command=lambda: popup_add(odrzavanjeMenu, 'odrzavanje.txt'))
odrzavanjeAdd.grid(column=2, row=17, padx=10, pady=10)
odrzavanjeMenu.current()

PrintButton = Button(master, text="ŠTAMPAJ", width=43, command=lambda: printer())
PrintButton.place(relx=0.36, rely=0.76)

sabloniListbox = Listbox(master, width=45, height=30, selectmode=SINGLE)
sabloniListbox.place(relx=0.72, rely=0.02)

scrolly = tk.Scrollbar(master, command=canvas.yview)
scrolly.place(relx=1, rely=0, relheight=1, anchor='ne')


def update_listbox(*args):
    list1 = []
    choices = sabloniListbox.get(0, END)
    pattern = search_var.get()
    if pattern == '':
        sabloniListbox.delete(0, END)
        loadpresets()
    else:
        with open('data_folder/sabloni.txt', 'rb') as f:
            try:
                data = pickle.load(open("data_folder/sabloni.txt", "rb"))
            except EOFError:
                data = []
            for dictionary in data:
                list1.append(dictionary['preset_name'])
        choices = list1
        choices = [x for x in choices if x.startswith(pattern)]
        sabloniListbox.delete(0, END)
        sabloniListbox.insert(END, *choices)


search_var = tk.StringVar()
search_var.trace('w', update_listbox)

label1 = Label(master, text="PRETRAGA:")
label1.place(relx=0.74, rely=0.85)

searchbox = Entry(master, textvariable=search_var)
searchbox.place(relx=0.81, rely=0.85)

sabloniListbox.config(yscrollcommand=scrolly.set)
scrolly.config(command=sabloniListbox.yview)

exportLabel = Label(master, text="IME ŠABLONA:")
exportLabel.place(relx=0.36, rely=0.70)

export_name = tk.StringVar()
exportUnos = ttk.Entry(master, width=15, textvariable=export_name)
exportUnos.place(relx=0.45, rely=0.70)

ExportButton = Button(master, text="IZVEZI ŠABLON", command=lambda: exporter(exportUnos.get()))
ExportButton.place(relx=0.56, rely=0.695)

ImportButton = Button(master, text="UVEZI ŠABLON", command=lambda: importer())
ImportButton.place(relx=0.72, rely=0.92)

DeleteButton = Button(master, text="OBRIŠI ŠABLON", command=lambda: delete_preset())
DeleteButton.place(relx=0.88, rely=0.92)

porekloMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('poreklo', porekloMenu.get()))
uvoznikMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('uvoznik', uvoznikMenu.get()))
proizvodjacMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('proizvodjac', proizvodjacMenu.get()))
uverenjeMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('uverenje', uverenjeMenu.get()))
nazivMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('naziv', nazivMenu.get()))
artikalMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('artikal', artikalMenu.get()))
liceMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('lice', liceMenu.get()))
postavaMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('postava', postavaMenu.get()))
djonMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('djon', djonMenu.get()))
srpsMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('srps', srpsMenu.get()))
izradaMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('izrada', izradaMenu.get()))
namenaMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('namena', namenaMenu.get()))
odrzavanjeMenu.bind('<<ComboboxSelected>>', lambda _: form_preview('odrzavanje', odrzavanjeMenu.get()))

loadpresets()

mainloop()
