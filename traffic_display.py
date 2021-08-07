import json
from functools import partial
from tkinter import *

from dotmap import DotMap

from traffic_base import tm_init, tm_get_street, tm_next_step
from traffic_display_components import TkStreet

f = open("model_01.json")
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
        crossing_frame = Frame(root, bg='white')
        crossing_frame.grid()
        tk_crossing_label = Label(crossing_frame, text=crossing.name, font=("Courier", 22), bg='white')
        tk_crossing_label.grid(row=0, column=0, padx=4, pady=4, sticky=N + W)
        tk_crossing_controls = Frame(crossing_frame)
        tk_crossing_controls.grid(row=1, column=1, rowspan=len(crossing.in_list), sticky=N + S + W + E)
        index = 0
        for situation in crossing.green_situations:
            b = Button(tk_crossing_controls, text="\n".join(situation), highlightbackground='gray',
                       command=partial(tm_set_green, crossing, index))
            b.pack()
            crossing.tk_buttons.append(b)
            index += 1

        z = 1
        street_set = set()
        for in_street in crossing.in_list:
            street_set.add(in_street)
            street = tm_get_street(tm, in_street)
            tk_street_parent = Frame(crossing_frame)
            street.tk_street = TkStreet(tk_street_parent, street)
            street.tk_street.grid()
            tk_street_parent.grid(row=z, column=0, sticky=N + S + W + E)

            lf_out = Frame(tk_street_parent)
            lf_out.grid(row=0, column=street.length + 1, rowspan=2, )
            i = 0
            for out in tm.in_outs[street.name]:
                lo = Label(lf_out, text=out, bg="red", fg="white")
                lo.grid(row=i, column=0)
                i += 1
            z += 1

        for line in crossing.lines:
            if line.out not in street_set:
                street_set.add(line.out)
                street = tm_get_street(tm, line.out)
                tk_street_parent = Frame(crossing_frame)
                street.tk_street = TkStreet(tk_street_parent, street)
                street.tk_street.grid()
                tk_street_parent.grid(row=z, column=0, sticky=N + S + W + E)
                z += 1

    buttons = Frame(root)
    buttons.grid()

    def _next_fun():
        tm_next_step(tm)
        refresh_tk(tm)

    next = Button(buttons,
                  text="next_step",
                  command=_next_fun)
    next.grid(row=0, column=0)

    refresh_tk(tm)

    root.mainloop()


def refresh_tk(tm):
    for street in tm.streets:
        for i, car in enumerate(street.slots):
            street.tk_slots[i].set_car(car)


start_traffic_display(tm)
