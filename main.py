#!/usr/bin/env python

'''
main.py: This file was developed for 2018hashcode competition to optimise the scheduling of driverless cars. It reads
from a data file with defined list of tasks and cars and returns a task schedule for each car.
'''
__author__ = "李青林， 王点点， 吴雨航"
__credits__ = "Sitong An"
__version__ = "1.0.1"
__status__ = "Developing"


class Task(object):
    def __init__(self, no, a, b, x, y, s, f):
        self.no = no
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.start = (a, b)
        self.end = (x, y)
        self.s = s
        self.f = f
        self.distance = self.distance()
        self.latest_s = self.latest_s()
        self.done = False

    def distance(self):
        return abs(self.x - self.a) + abs(self.y - self.b)

    def latest_s(self):
        return self.f - self.distance

    def taken(self):
        self.done = True




class Car(object):
    def __init__(self, label):
        self.label = label
        self.position = (0,0)
        self.avai_in = 0
        self.lazy = True
        self.task_history = []
        self.D = 0      # distance to current task being considered

    def take_task(self, task, time):
        self.lazy = False
        position_to_task = abs(task.start[0]-self.position[0]) + abs(task.start[1] - self.position[1])
        self.position = task.end
        self.avai_in = max(position_to_task, task.s - time) + task.distance
        self.task_history.append(task.no)

    def move(self):
        if self.lazy:
            pass
        else:
            self.avai_in -= 1
            if self.avai_in == 0:
                self.lazy = True


# function to read input and sort the sequence of tasks
def read_input(path):
    tasks_data = []
    with open(path, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if i == 0:
            spec = list(map(int, line[:-1].split(' ')))
        else:
            row = list(map(int, line[:-1].split(' ')))
            tasks_data.append(Task(i-1, row[0], row[1], row[2], row[3], row[4], row[5]))
            sequence = sorted(tasks_data, key=get_ls)
    return spec, sequence


def get_ls(ob):
    return ob.latest_s

# initialisation
file_name = 'b_should_be_easy'
path = file_name + '.in'  #change accodingly to read different files.
spec, l_task = read_input(path)
t = 0
T = spec[5]
N_lazy = spec[2]
N_taskdone = 0
# Build list of objects Car.
l_car = []
for car in range(0, N_lazy):
    l_car.append(Car(car))


def assign(l_task, l_car, i):
    if l_task[i].done:
        return None, None
    else:
        ls = l_task[i].latest_s
        ok_car = []
        for car in l_car:
            if car.lazy:
                car.D = abs(l_task[i].a - car.position[0]) + abs(l_task[i].b - car.position[1])
                if car.D < ls - t:
                    ok_car.append(car)
        if not ok_car:
            return None, None
        else:
            def newD(obj):
                return abs(obj.D + t - l_task[i].s)
            sortedCar = sorted(ok_car, key=newD)
            return l_task[i], sortedCar[0]

# main function, Qinglin refuse to put it into a run() method of a class
while t < T:
    for car in l_car:
        car.move()
    for i in range(0, len(l_task)):
        which_task, which_car = assign(l_task, l_car, i)
        if which_car:
            which_car.take_task(which_task, t)
            which_task.taken()
    t += 1
    print(t)



def output(path):
    with open(path, 'w') as f:
        for car in l_car:
            row = str(len(car.task_history)) + ' ' + ' '.join(map(str, car.task_history))
            f.write(row + '\n')

output(file_name+'.out')


