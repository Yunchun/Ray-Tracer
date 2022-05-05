import random

infinity = float('inf')
pi = 3.1415926535897932385

def degrees_to_radians(degrees: float):
    return degrees * pi / 180.0

def rand_double():
    # Returns a random real in [0,1)
    return random.random()

def random_double(min: float, max: float):
    # Returns a random real in [min,max]
    return min + (max-min) * rand_double()

def random_int(min: int, max: int):
    # Returns a random integer in [min, max]
    return int(random_double(min, max + 1))

def clamp(x: float, min: float, max: float):
    if x < min:
        return min
    if x > max:
        return max
    return x

    