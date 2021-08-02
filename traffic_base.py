from random import uniform, randrange

from dotmap import DotMap

MAX_VELOCITY = 10
HIT_BREAK_PERCENTAGE = 0.2


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

    tm_consolidate_streets_and_cars(tm)

    return tm


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
                        ri = randrange(0, len(outs))
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
    tm.all_cars.append(car)
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


def next_free_slot(start_pos, slots):
    d = 0

    while True:
        d += 1
        if start_pos + d < len(slots):
            if slots[start_pos + d] is None:
                pass
            else:
                break
        else:
            break
    return d - 1


def tm_get_street(tm, name):
    if name == tm.nirvana.name:
        return tm.nirvana
    return [street for street in tm.streets if street.name == name][0]


def tm_next_step_street(tm, street, green_streets):
    for slot in street.slots:
        if slot is not None:
            car = slot
            n = []
            if car.next_street in green_streets:
                n = tm_get_street(tm, car.next_street).slots
            cancat_slots = street.slots + n
            d0 = next_free_slot(car.pos, cancat_slots)
            t = min(car.velocity + 1, d0, MAX_VELOCITY)
            velocity = max(car.velocity - 1, 0) if uniform(0, 1) < HIT_BREAK_PERCENTAGE else t
            car.velocity = velocity
            new_pos = car.pos + car.velocity
            if new_pos < len(street.slots):
                car.pos = new_pos
            else:
                car.street = car.next_street
                car.pos = new_pos - len(street.slots)
                car.next_street = ""


def tm_next_step(tm):
    tm_update_green_in_outs(tm)

    for street in tm.streets:
        out_greens = [tm.nirvana.name]
        if street.name in tm.in_outs:
            out_greens = tm.green_in_outs[street.name]
        tm_next_step_street(tm, street, out_greens)

    tm_consolidate_streets_and_cars(tm)

    return tm


def create_new_slots(length):
    return [None] * length
