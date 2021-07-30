


from traffic_base import Car, next_step, tm_init, create_cars
import json
from random import uniform, shuffle
import matplotlib.pyplot as plt
import numpy as np
from dotmap import DotMap
f = open("modell_0.1.json")


traffic_model = DotMap(json.load(f))
print(traffic_model.name)
tm_init(traffic_model)
create_cars(traffic_model)
print(traffic_model)

def cars_to_numbers(cars):
    numbers = []
    for car in cars:
        if car is None:
            numbers.append(-1)
        else:
            numbers.append(car.v)
    return numbers

L = 20 # number of cells in row
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


for i in range(20):
    prev = iterations[-1]
    curr = next_step(prev, dict())
    iterations.append(curr)


a = np.zeros(shape=(len(iterations),L))
for i in range(L):
    for j in range(len(iterations)):
        a[j,i] = 1 if iterations[j][i] is not None else 0

# showing image
plt.imshow(a, cmap="Greys", interpolation="none")
plt.show()