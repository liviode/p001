import json
from functools import partial
from tkinter import *
from tkinter import ttk

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
    root.geometry("800x300")
    root.config(bg="white")
    for crossing in tm.crossings:

        street_set = set()
        for line in crossing.lines:
            street_set.add(line['in'])
            street_set.add(line['out'])

        crossing.tk_buttons = []
        crossing_frame = Frame(root, bg='white')
        crossing_frame.grid(padx=50, pady=10)
        tk_crossing_label = Label(crossing_frame, text=crossing.name, font=("Courier", 22), bg='white')
        tk_crossing_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        tk_controls_frame = Frame(crossing_frame)
        tk_controls_frame.grid(row=1, column=2, rowspan=len(street_set)*2, sticky=N + S + W + E)

        for i, situation in enumerate(crossing.green_situations):
            b = Button(tk_controls_frame, text="\n".join(situation), highlightbackground='gray',
                       command=partial(tm_set_green, crossing, i))
            b.grid(column=0, row=i, padx=10, pady=10)
            crossing.tk_buttons.append(b)

        row = 1
        street_set = set()
        for in_street in crossing.in_list:
            street_set.add(in_street)
            street = tm_get_street(tm, in_street)
            tk_street_frame = Frame(crossing_frame)
            tk_street_frame.grid(row=row, column=0, pady=10, sticky=N + S + W + E)
            sep = ttk.Separator(crossing_frame, orient=VERTICAL)
            sep.grid(row=row + 1, column=0, sticky=N + S + W + E)

            street.tk_street = TkStreet(tk_street_frame, street)
            street.tk_street.grid()

            outs_frame = Frame(crossing_frame)
            outs_frame.grid(row=row, column=1, padx=10, pady=10)
            sep = ttk.Separator(crossing_frame, orient=VERTICAL)
            sep.grid(row=row + 1, column=1, sticky=N + S + W + E)

            i = 0
            for out in tm.in_outs[street.name]:
                lo = Label(outs_frame, text=out, bg="red", fg="white")
                lo.grid(row=0, column=i, padx=10, pady=10)
                i += 1
            row += 2

        for line in crossing.lines:
            if line.out not in street_set:
                street_set.add(line.out)
                street = tm_get_street(tm, line.out)
                tk_street_frame = Frame(crossing_frame)
                tk_street_frame.grid(row=row, column=0, pady=10, sticky=N + S + W + E)
                sep = ttk.Separator(crossing_frame, orient=VERTICAL)
                sep.grid(row=row+1, column=0, columnspan=2, sticky=N + S + W + E)

                street.tk_street = TkStreet(tk_street_frame, street)
                street.tk_street.grid()

                row += 2

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
