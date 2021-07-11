
import tkinter as tk

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 400, height = 300,  relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='Crossings')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Number of crossings:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry (root)
entry2 = tk.Entry (root)
canvas1.create_window(200, 140, window=entry1)
canvas1.create_window(200, 300, window=entry2)
def getSquareRoot ():

    x1 = entry1.get()

    label3 = tk.Label(root, text= 'The Square Root of ' + x1 + ' is:',font=('helvetica', 10))
    canvas1.create_window(200, 210, window=label3)

    label4 = tk.Label(root, text= float(x1)**0.5,font=('helvetica', 10, 'bold'))
    canvas1.create_window(200, 230, window=label4)

button1 = tk.Button(text='Get the Square Root', command=getSquareRoot, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)

root.mainloop()

a_dictionary = {}



for number in range(1,10):
    xd = 2 * number
    a_dictionary["key%s" %number] = xd

print(a_dictionary)


traffic = {
    'streets': [{'name': 's1'}, {'name': 's2'}, {'name': 's3'}, {'name': 's4'}, {'name': 's5'}],
    'crossings': [{'name': 'c1',
                   'lines': [
                       {'name': '1->5', 'in': 's1', 'out': 's5', 'frequency': 5},
                       {'name': '3->2', 'in': 's3', 'out': 's2', 'frequency': 41},
                       {'name': '3->5', 'in': 's3', 'out': 's5', 'frequency': 55}

                   ],
                   'green_situations': [['1->5', '3->2'], ['3->5'], ['4->2'], ]},
                  {'name': 'c2',
                   'lines': [],
                   'green_situations': []}
                  ]
}

cross = {}
for n in traffic['crossings']:
   print(n['lines'])
   for l in n['lines']:
       print('  ', l['name'])
       for number in range(1,10):
            cross['coordinates', number ] = 10 + int(number)



print(cross)
