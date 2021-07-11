import json
import math

# dictionary for crossings, streets and greensituation

traffic = {
    "streets": [{'name': 's1'}, {'name': 's2'}, {'name': 's3'}, {'name': 's4'}, {'name': 's5'}],
    'crossings': [{'name': 'c1',
                   'lines': [
                       {'name': '1->5', 'in': 's1', 'out': 's5', 'frequency': 5},
                       {'name': '3->2', 'in': 's3', 'out': 's2', 'frequency': 41},
                       {'name': '3->5', 'in': 's3', 'out': 's5', 'frequency': 55},
                       {'name': '4->2', 'in': 's4', 'out': 's2', 'frequency': True},
                      {'name': '4->1', 'in': 's4', 'out': 's5', 'frequency': True}
                   ],
                   'green_situations': [['1->5', '3->2'], ['3->5'], ['4->2'], ['4->1'] ]},
                  {'name': 'c2',
                   'lines': [{'name': '1->5', 'in': 's1', 'out': 's5', 'frequency': 5}],
                   'green_situations': [
                       ['1->5']
                   ]}

                  ]
}

print('orig', type(traffic), traffic)

d = json.dumps(traffic)

print('dumps', type(d), d)

l = json.loads(d)

print('loads', type(l), l)


from tkinter import *

master = Tk()
master.title("crossing")

# canvas properties
canvas_width = 900
canvas_height = 900
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)

w.pack()

# points on crossing
def street_dot(x0, y0, x1, y1, alpha):
    r = (x1 - x0) / 2
    x = r * math.cos(alpha)
    y = r * math.sin(alpha)
    x = x + x0 + r
    y = y + y0 + r
    return x, y
# center of the crossing
def text_point(x0, y0, x1, y1, dx, dy, length):
    x0 = (x0 + x1)/2
    y0 = (y0 + y1)/2
    x0 = dx-x0
    y0 = dy-y0
    x = dx + length * x0
    y = dy + length * y0
    return (x,y)


# circle properties
crossing_number = 1
gap = 100
diameter = 100

for c in traffic['crossings']:
    print(c['name'])
    print('lines')
    # crossing oval ...
    x0 = gap * crossing_number
    y0 = gap * crossing_number
    x1 = gap * crossing_number + diameter
    y1 = gap * crossing_number + diameter
    w.create_oval(x0, y0, x1, y1)
    a_dictionary = {"key%s"}
    crossing_number += 1

    line_number = 0
    ins = set()
    outs = set()
    for line in c['lines']:
        ins.add(line['in'])
        outs.add(line['out'])
    numbers_of_insouts = len(ins) + len(outs)

    # connection circles
    alpha = 0
    conn_to_point = {}
    for conn in sorted(ins):
        xd, yd = street_dot(x0, y0, x1, y1, alpha)
        alpha = alpha + 2 / numbers_of_insouts * math.pi
        w.create_oval(xd - 2, yd - 2, xd + 2, yd + 2)
        conn_to_point[conn] = (xd, yd)

        w.create_text(*text_point(x0,y0,x1,y1,xd,yd, 0.2), text=conn)

    for conn in sorted(outs):
        xd, yd = street_dot(x0, y0, x1, y1, alpha)
        alpha = alpha + 2 / numbers_of_insouts * math.pi
        w.create_oval(xd - 2, yd - 2, xd + 2, yd + 2)
        conn_to_point[conn] = (xd, yd)
        w.create_text(*text_point(x0,y0,x1,y1,xd,yd, 0.2), text=conn)

    # connection lines
    for line in c['lines']:
        conn_in = line['in']
        conn_out = line['out']
        start_point = conn_to_point[conn_in]
        end_point = conn_to_point[conn_out]
        w.create_line(*start_point, *end_point)

    print('green_situations')
    for gs_list in c['green_situations']:
        print('-')
        for gs in gs_list:
            print('  ', gs)

# x = 100
# y = 100
# pi = math.pi
# for s in traffic['streets']:
#     print(s['name'])
#     w.create_oval(x, y, x + 100 , y + 100, fill="#476042")
#     x = x + 100
#     y = y + 100
# print(math.pi)



def main():
    mainloop()


if __name__ == "__main__":
    main()
