import math


def is_prime(n):
    if(n < 2):
        return False
    if(n == 2):
        return True
    if(n % 2 == 0):
        return False

    for i in range(3, math.sqrt(n), 2):
        if(n % i == 0):
            return False

    return True


def next_prime(n):
    n = n + 1
    while(not is_prime(n)):
        n = n + 1

    return n


def previous_prime(n):
    n = n - 1
    while(not is_prime(n)):
        n = n - 1

    return n
