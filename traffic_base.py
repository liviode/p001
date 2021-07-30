from random import uniform, randint
from dotmap import DotMap


def tm_init(tm):
    tm.step = 0
    tm.all_cars = []
    tm.car_counter = 0
    tm.street_map = DotMap()
    tm.green_in_outs = None

    tm.nirvana = DotMap()
    tm.nirvana.name = "nirvana"
    tm.nirvana.length = 10
    tm.nirvana.slots = create_new_slots(tm.nirvana.length)
    tm.nirvana.density = 0

    for street in tm.streets:
        street.slots = create_new_slots(street.length)

    tm.in_outs = DotMap()
    for crossing in tm.crossings:
        crossing.green_situations_index = -1
        in_set = set()
        for line in crossing.lines:
            _in = line["in"]
            tm.in_outs[_in] = [] if _in not in tm.in_outs else tm.in_outs[_in]
            tm.in_outs[_in].append(line.out)
            in_set.add(_in)
        crossing.in_list = list(in_set)
        crossing.in_list.sort()


def tm_create_cars(tm):
    for street in tm.streets:
        if street.slots[0] is None and uniform(0, 1) <= street.density:
            car = new_car(tm)
            car.street = street.name
            car.pos = 0
            street.slots[0] = car


def tm_consolidate_streets_and_cars(tm):
    tm_create_cars(tm)
    for street in tm.streets:
        street.slots = create_new_slots(street.length)
        outs = tm.in_outs[street.name] if tm.in_outs.has_key(street.name) else None
        for car in tm.all_cars:
            if car.street == street.name:
                street.slots[car.pos] = car
                if car.next_street == "":
                    if outs is not None:
                        ri = randint(0, len(outs))
                        car.next_street = outs[ri]
                    else:
                        car.next_street = tm.nirvana.name


def new_car(tm):
    car = DotMap()
    car.nr = tm.car_counter
    car.velocity = 0
    car.street = ''
    car.pos = -1
    car.next_street = ""
    tm.car_counter += 1
    return car


def tm_update_green_in_outs(tm):
    tm.green_in_outs = DotMap()
    for crossing in tm.crossings:
        green_lines = []
        if crossing.green_situations_index != -1:
            green_lines = crossing.green_situations[crossing.green_situations_index]
        for line in crossing.lines:
            line_in = line['in']
            if not tm.green_in_outs.has_key(line_in):
                tm.green_in_outs[line_in] = []
            if line.name in green_lines:
                tm.green_in_outs[line_in].append(line.out)




def tm_next_step(tm):
    tm_update_green_in_outs(tm)

    L = len(prev)
    vmax = 3
    p = 0.2
    curr = [None] * L
    nextstreet = [None] * 100
    for x in range(L):

        if prev[x] is not None:
            car = prev[x]
            vi = car.v
            d = 1
            while prev[(x + d) % L] is None and (x + d) < L:
                d += 1
                if (x + d) < L:
                    pass
                else:
                    street = car.get_next_street()

                    if street in green_streets and nextstreet[(x + d) % L] is None:
                        # check if empty space for car exists in street
                        nextstreet.append(car)


                    else:
                        break

            vtemp = min(vi + 1, d - 1, vmax)  # increse speed up to max speed, but don't move further than next car

            v = max(vtemp - 1, 0) if uniform(0,
                                             1) < p else vtemp  # with probability p hit the brakes, otherwise sustain velocity
            if (x + v) >= L:
                print(x + v)
            curr[(x + v) % L] = car
            car.v = v
            car.pos = x
    return curr


def tm_next_step_street(tm, street, out_greens):
    pass


def create_new_slots(length):
    return [None] * length
