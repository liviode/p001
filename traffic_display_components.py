import tkinter as tk

class TkCar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.car = tk.Label(self, text='-', anchor="w")
        self.velocity = tk.Label(self, text='-', anchor="e")
        self.car.pack()
        self.velocity.pack( )

    def get(self):
        return self.entry.get()

    def set_car(self, car):
        if car is None:
            self.car['text'] = '-'
            self.velocity['text'] = '-'
        else:
            self.car['text'] = car.nr
            self.velocity['text'] = car.velocity



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
