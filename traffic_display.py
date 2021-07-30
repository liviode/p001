from tkinter import *
from dotmap import DotMap
from traffic_base import tm_init
from tkinter.messagebox import *
import json

from functools import partial

f = open("model-enge.json")
tm = DotMap(json.load(f))
tm_init(tm)


def tm_set_green(crossing, index):
    crossing.green_situations_index = index
    for b in crossing.tk_buttons:
        b.config(highlightbackground='red')
    crossing.tk_buttons[index].config(highlightbackground='green')


def start_traffic_display(tm):
    root = Tk()
    root.title("PythonGuides")
    root.geometry("400x300")
    root.config(bg="#9FD996")
    for crossing in tm.crossings:
        crossing.tk_buttons = []
        crossing_frame = Frame(root)
        crossing_frame.pack(fill="both", expand="yes")
        l0 = Label(crossing_frame, text=crossing.name, bg="white")
        l0.grid(row=0, column=0)
        fb = Frame(crossing_frame)
        fb.grid(row=1, column=1, rowspan=len(crossing.in_list), sticky=N + S + W + E)
        index = 0
        for situation in crossing.green_situations:
            b = Button(fb, text="\n".join(situation), highlightbackground='gray',
                       command=partial(tm_set_green, crossing, index))
            b.pack()
            crossing.tk_buttons.append(b)
            index += 1

        z = 1
        for in_street in crossing.in_list:
            street = tm.street_map[in_street]
            lf = Frame(crossing_frame)
            lf.grid(row=z, column=0, sticky=N + S + W + E)
            z += 1
            l0 = Label(
                lf,
                text=street.name,
                bg="blue",
                fg="white"
            )
            l0.grid(row=0, column=0, columnspan=street.length, rowspan=1, sticky=N + S + W + E)
            street.tk_labels = []
            for i in range(street.length):
                l1 = Label(
                    lf,
                    text=i,
                    bg="#9FD996"
                )
                street.tk_labels.append(l1)
                l1.grid(row=1, column=i)
            lf_out = Frame(lf)
            lf_out.grid(row=0, column=street.length + 1, rowspan=2, )
            i = 0
            for out in tm.in_outs[street.name]:
                lo = Label(lf_out, text=out, bg="red", fg="white")
                lo.grid(row=i, column=0)
                i += 1

    root.mainloop()


start_traffic_display(tm)
