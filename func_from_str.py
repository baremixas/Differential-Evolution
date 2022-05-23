from math import tan, atan, e, pi
import numpy as np

def sin(x):
    return np.sin(x)

def asin(x):
    return np.arcsin(x)

def cos(x):
    return np.cos(x)

def tan(x):
    return np.tan(x)

def atan(x):
    return np.arctan(x)

def sqrt(x):
    return np.sqrt(x)

def func_read(list,element):
    x = element
    function_vals = []

    for fun in list:
        try:
            function_vals.append(eval(fun))
        except:
            print("Invalid input function: ", fun)
            continue

    return function_vals
