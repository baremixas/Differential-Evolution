import numpy as np
from check_restrictions import check_restrictions

def crossover(element, iteration, population, num_arg, CR, func_list, bounds):
    valid = False

    while valid == False:
        valid = True

        el1 = population[iteration]
        el2 = element

        crossed = []
        for i in range(num_arg):
            if np.random.uniform(0.0,1.0,1) < CR:
                crossed.append(el2[i])
            else:
                crossed.append(el1[i])

        valid = check_restrictions(crossed, num_arg, func_list, bounds)

    return crossed
