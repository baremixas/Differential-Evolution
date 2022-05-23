import numpy as np
from check_restrictions import check_restrictions

def mutation(iteration, population, num_arg, F, func_list, bounds):
    valid = False

    elements = [element for element in range(len(population)) if element != iteration]

    while valid == False:
        valid = True

        # a można dobrać jako best z populacji
        a = population[np.random.choice(elements)]
        b = population[np.random.choice(elements)]
        c = population[np.random.choice(elements)]

        mutated = []

        for i in range(num_arg):
            mutated.append(a[i] + F * (b[i] - c[i]))

        valid = check_restrictions(mutated, num_arg, func_list, bounds)

    return mutated
