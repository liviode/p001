from tkinter import *
from dotmap import DotMap
import json

f = open("modell_0.1.json")
tm = DotMap(json.load(f))


def start_traffic_display(tm):
    root = Tk()
    scrollbar = Tk.Scrollbar(root)
    root.title("PythonGuides")
    root.geometry("400x300")
    root.config(bg="#9FD996")
    for street in tm.streets:
        lf = LabelFrame(root, text="xyz", scrollbar=True)
        lf.pack(fill="both",expand ="yes")
        l0 = Label(
            lf,
            text=street.name,
            bg="#9FD996"
        )
        l0.grid(row=0, column=0, columnspan=street.length, ipady=0)

        street.tk_labels = []
        for i in range(street.length):
            l1 = Label(
                lf,
                text=i,
                bg="#9FD996"
            )
            street.tk_labels.append(l1)
            l1.grid(row=1, column=i)

    root.mainloop()
start_traffic_display(tm)
