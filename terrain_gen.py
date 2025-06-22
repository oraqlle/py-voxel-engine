from settings import CENTER_Y
from noise import noise2, noise3
from random import random
from numba import njit


@njit
def get_height(x, z):
    # amplitude
    a1 = CENTER_Y

    # frequency
    f1 = 0.005

    height = 0
    height += noise2(x * f1, z * f1) * a1 + a1

    return int(height)
