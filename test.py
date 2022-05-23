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

x = [-1, 1]
# fun = ['sin(x[1]) * e ** (1 - cos(x[0]) ** 2.0) + cos(x[0]) * e ** (1 - sin(x[1]) ** 2.0) + (x[0] - x[1]) ** 2']
fun = ['sqrt(3)']

def obj_f(x, function):
    fun = 0

    try:
        fun = eval(function)
    except:
        print("Invalid input function: ", function)

    return fun

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

print(type(obj_f(x,fun[0])))
print(obj_f(x,fun[0]))
