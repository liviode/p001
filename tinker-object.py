

from random import uniform, shuffle
import matplotlib.pyplot as plt
import numpy as np

sys.path.append("/Users/liviodecapitan/projects/tkinter.py")

from traffic-base import Car

def cars_to_numbers(cars):
    numbers = []
    for car in cars:
        if car is None:
            numbers.append(-1)
        else:
            numbers.append(car.v)
    return numbers


L = 500 # number of cells in row
num_iters = 500 # number of iterations
density = 0.2 # how many positives
vmax = 10
# probability of breaking randomly
p = 0.2
#Signal position
sig_pos = 250
#Signal Status
sig_stat = True

sig_temp = 10
sig_temp_off = 40
sig_temp_on = 13


cars_num = int(density * L)
initial0 = [0] * cars_num + [-1] * (L - cars_num)
initial = []
for i in initial0:
    if i == 0:
        initial.append(Car())
    else:
        initial.append(None)


shuffle(initial)

iterations = [initial]

for i in range(num_iters):
    prev,curr = iterations[-1],[None] * L
    #Lichtsignal
    if sig_stat:
        sig_temp = sig_temp + 1
    else:
        sig_temp = sig_temp -1

    if sig_temp > sig_temp_on:
        sig_temp = 0
        sig_stat = False
    if sig_temp < -sig_temp_off:
        sig_temp = 0
        sig_stat = True




    for x in range(L):
        if prev[x] is not None:
            car = prev[x]
            vi = car.v
            d = 1
            while prev[(x + d) % L] is None:
                d += 1
            #Lichtsignal
            if sig_stat:
                ds = sig_pos - x
                ds = d if ds < 1 else ds
                d = min(ds, d)




            vtemp = min(vi+1, d - 1, vmax) # increse speed up to max speed, but don't move further than next car



            v = max(vtemp - 1, 0) if uniform(0,1) < p else vtemp # with probability p hit the brakes, otherwise sustain velocity
            #curr[(x + v) % L] = v # perform the move
            curr[(x + v) % L] = car
            car.v = v
        #print(x,v)

    iterations.append(curr)


a = np.zeros(shape=(num_iters,L))
for i in range(L):
    for j in range(num_iters):
        a[j,i] = 1 if iterations[j][i] is not None else 0

# showing image
plt.imshow(a, cmap="Greys", interpolation="nearest")
plt.show()