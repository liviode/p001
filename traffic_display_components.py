import tkinter as tk


class TkCar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.car = tk.Label(self, text='-', anchor="e")
        self.velocity = tk.Label(self, text='-', anchor="w")

        self.car.pack(ipadx=2,
                      ipady=2,
                      expand=True,
                      fill='both',
                      side='left')
        self.velocity.pack(ipadx=2,
                           ipady=2, fill='both')

    def set_car(self, car):
        if car is None:
            self.car['text'] = '-'
            self.velocity['text'] = '-'
            self.car.config(bg='gray')
            self.velocity.config(bg='gray')
        else:
            self.car['text'] = car.nr
            self.velocity['text'] = car.velocity
            self.car.config(bg='white', borderwidth=1)
            self.velocity.config(bg='yellow')


if __name__ == '__main__':
    print('hello main')
    root = tk.Tk()
    tkcar = TkCar(root)
    tkcar.pack()


    def car():
        pass


    car.nr = 25
    car.velocity = 2
    tkcar.set_car(car)
    root.mainloop()
