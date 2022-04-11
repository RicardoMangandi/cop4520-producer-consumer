from cmath import sqrt
import time


def is_prime(n):

    if (n <= 1):
        return False
    
    for i in range(2,n):
        if (n % i == 0):
            return False
    return True


def do_task_function(param1,param2):
    total = 0
    for i in range(param1,param2):
        if is_prime(i):
            total = total + i 
    
    return total

