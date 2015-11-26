import sys
import colorlist

from tkinter import *

app = Tk()
cbox = Listbox(app)

# Add data
data = colorlist.load()
keys = list(data.keys())
keys.sort()
for key in keys:
    cbox.insert(END, key)
cbox.pack(padx=64, pady=64)

# Hook selection
cbox.bind('<<ListboxSelect>>', lambda *args : app.config(bg=data[cbox.get(int(cbox.curselection()[0]))]))

app.mainloop()
