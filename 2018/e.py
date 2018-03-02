#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import sys
from collections import namedtuple


random.seed(None)

Metadata = namedtuple('Metadata', ['R', 'C', 'F', 'N', 'B', 'T'])
CarState = namedtuple('CarState', ['x', 'y', 't'])


class Ride(object):
    def __init__(self, i, a, b, x, y, s, f):
        self.i = i
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.s = s
        self.f = f
        self.dist = distance_coord(a, b, x, y)


class Car(object):
    def __init__(self, index):
        self.index = index
        self.assigned_rides = []
        self.state = CarState(0, 0, 0)

    def min_start_time(self, ride):
        return max(ride.s, self.state.t + distance_coord(self.state.x, self.state.y, ride.a, ride.b))

    def can_add(self, ride):
        return self.min_start_time(ride) + ride.dist <= ride.f

    def adding_value(self, ride, B):
        if self.can_add(ride):
            min_start_time = self.min_start_time(ride)
            if min_start_time == ride.s:
                return B + ride.dist
            else:
                return ride.dist
        else:
            return 0

    def add(self, ride):
        can = self.can_add(ride)
        if not can:
            raise Exception("can't add ride!! %s" % ride.i)
        t = ride.dist + self.min_start_time(ride)
        self.state = CarState(ride.x, ride.y, t)
        self.assigned_rides.append(ride)


def read_input():
    metadata = Metadata(*map(int, input().split()))
    rides = []
    for i in range(metadata.N):
        rides.append(Ride(i, *list(map(int, input().split()))))
    return metadata, rides


def distance_coord(a,b,x,y):
    return abs(a-x) + abs(b-y)


def distance(a, b):
    return distance_coord(a.x, a.y, b.x, b.y)


def choose_assignment_from_best_cars(cars, ride):
    return max(cars, key=lambda c: c.state.t)


def solve(metadata, rides):
    cars = []
    for i in range(metadata.F):
        cars.append(Car(i))

    for ride in sorted(rides, key=lambda r: r.dist + r.s):
        car_assignments = []
        for car in cars:
            car_assignments.append((car.adding_value(ride, metadata.B), car))
        max_val = max(c[0] for c in car_assignments)
        if max_val > 0:
            best_cars = [c[1] for c in car_assignments if c[0] == max_val]
            car = choose_assignment_from_best_cars(best_cars, ride)
            car.add(ride)
    return cars


def print_solution(solution):
    for car in solution:
        rides = [ride.i for ride in car.assigned_rides if ride.i != None]
        print(len(rides), *rides)


def evaluate(solution, rides, B):
    score = 0
    for car in solution:
        state = CarState(0, 0, 0)
        for ride in car.assigned_rides:
            ride = rides[ride.i]
            arrive_t = state.t + distance_coord(state.x, state.y, ride.a, ride.b)
            finish_t = max(arrive_t, ride.s) + ride.dist
            if finish_t <= ride.f:
                score += ride.dist
                if arrive_t <= ride.s:
                    score += B
            else:
                sys.stderr.write("Added ride with no points!!", car.index, ride.i, car.state)
            state = CarState(ride.x, ride.y, finish_t)
    return score


if __name__ == "__main__":
    metadata, rides = read_input()
    solution = solve(metadata, rides)
    score = evaluate(solution, rides, metadata.B)
    sys.stderr.write(str(score)+'\n')
    print_solution(solution)