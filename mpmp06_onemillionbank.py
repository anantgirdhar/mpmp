import math
import numpy as np
import matplotlib.pyplot as plt

fibs_computed = {0: 0, 1: 1, 2: 1, 3: 2}

def fib(n):
    if n in fibs_computed.keys():
        return fibs_computed[n]
    result = fibs_computed.get(n-1, fib(n-1)) + fibs_computed.get(n-2, fib(n-2))
    fibs_computed[n] = result
    return result

def find_valid_deposits(target=1000000, return_solutions=False):
    # Try to find integer solutions to:
    # f_i d_1 + f_{i-1} d_2 = target
    # where f_i and f_{i-1} are consecutive fib numbers
    # and d_1 and d_2 are the variables to solve for
    # Assumes that d_1, d_2 are positive integers
    solutions = {}
    i = 32  # Gives fib numbers that are larger than 10^6
    while True:
        if i <= 1:
            break
        fi = fib(i)
        fiM1 = fib(i-1)
        # Check if either coefficient is larger than target
        # in which case no positive solution can be found
        if fi > target:
            i -= 1
            continue
        if fiM1 > target:
            i -= 1
            continue
        for d1 in range(math.floor(target/fi), 1, -1):
            d2 = (target - fi * d1) / fiM1
            int_d2 = int(d2)
            if abs(d2 - int_d2) < 1e-6:
                # It actually is an integer
                # This is a solution
                d2 = int_d2
                # If it is zero, it's not a valid solution
                if d2 == 0:
                    continue
                if not return_solutions:
                    print(f'i = {i}')
                    print(f'({fi}, {fiM1}) . ({d1}, {d2}) = {target}')
                    return i
                else:
                    if i not in solutions.keys():
                        solutions[i] = []
                    solutions[i].append((d1, d2))
        i -= 1
    if return_solutions:
        return solutions
    else:
        # If we are not returning solutions and we made it all the way here
        # then there are no solutions
        return 0

def solution_existance_plot():
    max_days_for_target = {i: find_valid_deposits(i) for i in range(100000)}
    keys = list(exist.keys())
    vals = list(exist.values())
    plt.plot(keys, vals, 'rx')
    plt.show()

