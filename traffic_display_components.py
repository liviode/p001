import tkinter as tk


class TkSlot(tk.Frame):

    def __init__(self, tk_parent):
        tk.Frame.__init__(self, tk_parent)

        self.car = tk.Label(self, text='-', anchor="e", width=1,font=("Courier", 12))
        self.velocity = tk.Label(self, text='-', anchor="w", width=1,font=("Courier", 12))

        self.car.pack(ipadx=2, ipady=2, expand=True, fill='both', side='left')
        self.velocity.pack(ipadx=2, ipady=2, fill='both')
        self.tooltop = ToolTip(self, text='')

    def set_car(self, car):
        if car is None:
            self.car['text'] = '-'
            self.velocity['text'] = '-'
            self.car.config(bg='gray')
            self.velocity.config(bg='gray')
            self.tooltop.text = '-'

        else:
            self.car['text'] = car.nr
            self.velocity['text'] = car.velocity
            self.car.config(bg='white', borderwidth=1)
            self.velocity.config(bg='yellow')
            self.tooltop.text = 'next_street:' + car.next_street


class TkStreet(tk.Frame):

    def __init__(self, tk_parent, street):
        tk.Frame.__init__(self, tk_parent)
        tk_street_label = tk.Label(tk_parent, text=street.name, fg="gray", font=("Courier", 18)
                                   )
        tk_street_label.grid(row=0, column=0, columnspan=street.length, rowspan=1, padx=(2, 2), pady=(2, 2),
                             sticky=tk.N + tk.W)
        self.index = 0

        street.tk_slots = []
        for i in range(street.length):
            tk_slot = TkSlot(self)
            street.tk_slots.append(tk_slot)
            tk_slot.grid(row=1, column=i)


class ToolTip:
    def __init__(self, widget, text=None):
        def on_enter(event):
            self.tooltip = tk.Toplevel()
            self.tooltip.overrideredirect(True)
            self.tooltip.geometry(f'+{event.x_root + 15}+{event.y_root + 10}')

            self.label = tk.Label(self.tooltip, text=self.text)
            self.label.pack()

        def on_leave(event):
            self.tooltip.destroy()

        self.widget = widget
        self.text = text

        self.widget.bind('<Enter>', on_enter)
        self.widget.bind('<Leave>', on_leave)






if __name__ == '__main__':
    print('hello main')
    
