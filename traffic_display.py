import json
from functools import partial
from tkinter import *
from traffic_display_components import TkCar

from dotmap import DotMap

from traffic_base import tm_init, tm_get_street, tm_next_step

f = open("modell_0.1.json")
tm = DotMap(json.load(f))
tm_init(tm)
for street in tm.streets:
    print(int(street.length))


def tm_set_green(crossing, index):
    crossing.green_situations_index = index
    for b in crossing.tk_buttons:
        b.config(highlightbackground='red')
    crossing.tk_buttons[index].config(highlightbackground='green')


def start_traffic_display(tm):
    root = Tk()
    root.title("PythonGuides")
    root.geometry("400x300")
    root.config(bg="white")
    for crossing in tm.crossings:
        crossing.tk_buttons = []
        crossing_frame = Frame(root)
        crossing_frame.grid()
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
            street = tm_get_street(tm, in_street)
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
            for i, car in enumerate(street.slots):
                tk_car = TkCar(lf)
                street.tk_labels.append(tk_car)
                tk_car.grid(row=1, column=i)
            lf_out = Frame(lf)
            lf_out.grid(row=0, column=street.length + 1, rowspan=2, )
            i = 0
            for out in tm.in_outs[street.name]:
                lo = Label(lf_out, text=out, bg="red", fg="white")
                lo.grid(row=i, column=0)
                i += 1
    buttons = Frame(root)
    buttons.grid()

    def _next_fun():
        tm_next_step(tm)
        refresh_tk(tm)

    next = Button(buttons,
                  text="next_step",
                  command=_next_fun)
    next.grid(row=0, column=0)

    root.mainloop()


def refresh_tk(tm):
    for street in tm.streets:
        for i, car in enumerate(street.slots):
            street.tk_labels[i].set_car(car)


start_traffic_display(tm)
