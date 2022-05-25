import copy
import matplotlib.pyplot as plt
import numpy as np

from math import e, pi

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


class DifferentialEvolution:
    def __init__(self):
        self.BOUNDS = []
        self.RESTRICT_FUNCTIONS = []

    def initialize_population(self):
        self.population = []

        for i in range(self.POPULATION_SIZE):
            valid = False
            while not valid:
                element = []

                # Generating random population elements
                for j in range(self.ARG_NUMBER):
                    if len(self.BOUNDS[j]) != 0:
                        element.append(float(np.random.uniform(self.BOUNDS[j][0], self.BOUNDS[j][1], 1)))
                    else:
                        element.append(float(np.random.uniform(-5, 5, 1)))

                valid = self.check_restrictions(element)

            self.population.append(element)

    @staticmethod
    def read_function(function_list, element):
        x = element
        function_vals = []

        for function in function_list:
            try:
                function_vals.append(eval(function))
            except:
                print("Invalid input function: ", function)
                continue

        return function_vals

    def check_restrictions(self, element):
        valid = True

        for i in range(self.ARG_NUMBER):
            if not self.BOUNDS[i]:
                if -5 <= element[i] <= 5:
                    continue
                else:
                    valid = False
            else:
                if self.BOUNDS[i][0] <= element[i] <= self.BOUNDS[i][1]:
                    continue
                else:
                    valid = False

        if len(self.RESTRICT_FUNCTIONS) != 0:
            for value in self.read_function(self.RESTRICT_FUNCTIONS, element):
                if value > 0:
                    valid = False

        return valid

    def mutation(self, iteration):
        valid = False

        elements = [element for element in range(len(self.population)) if element != iteration]

        while not valid:
            # a można dobrać jako best z populacji
            a = self.population[np.random.choice(elements)]
            b = self.population[np.random.choice(elements)]
            c = self.population[np.random.choice(elements)]

            mutated = []
            for i in range(self.ARG_NUMBER):
                mutated.append(a[i] + self.F * (b[i] - c[i]))

            valid = self.check_restrictions(mutated)

        return mutated

    def crossover(self, element, iteration):
        valid = False

        while not valid:
            el1 = self.population[iteration]
            el2 = element

            crossed = []
            for i in range(self.ARG_NUMBER):
                if np.random.uniform(0.0, 1.0, 1) < self.CR:
                    crossed.append(el2[i])
                else:
                    crossed.append(el1[i])

            valid = self.check_restrictions(crossed)

        return crossed

    def differential_algorithm(self):
        # Initialise random population within the specified bounds
        self.initialize_population()

        objective_function = [self.FUNCTION]

        # Calculate init fitness for population
        population_fitness = []
        for i in range(len(self.population)):
            population_fitness.append(self.read_function(objective_function, self.population[i])[0])

        loop = True
        loop_iteration = 0

        min_val = population_fitness[0]
        min_arg = self.population[0]
        min_arg_x1_list = []
        min_arg_x2_list = []

        while loop == True:
            for i in range(len(self.population)):
                el_mut = self.mutation(i)
                el_cross = self.crossover(el_mut, i)

                if self.read_function(objective_function, el_cross)[0] < population_fitness[i]:
                    self.population[i] = el_cross
                    population_fitness[i] = self.read_function(objective_function, el_cross)[0]

                if population_fitness[i] < min_val:
                    min_val = population_fitness[i]
                    min_arg = self.population[i]
                    min_arg_x1_list.append(min_arg[0])
                    min_arg_x2_list.append(min_arg[1])

            loop_iteration += 1
            if loop_iteration >= self.L:
                loop = False

        if self.ARG_NUMBER == 2:
            if len(self.BOUNDS[0]) != 0:
                x = np.linspace(self.BOUNDS[0][0], self.BOUNDS[0][1], 100)
            else:
                x = np.linspace(-5, 5, 100)
            if len(self.BOUNDS[1]) != 0:
                y = np.linspace(self.BOUNDS[1][0], self.BOUNDS[1][1], 100)
            else:
                y = np.linspace(-5, 5, 100)

            xx, yy = np.meshgrid(x, y)

            xy = [xx, yy]
            z = self.read_function(objective_function, xy)[0]

            for restrict in self.RESTRICT_FUNCTIONS:
                z[self.read_function([restrict], xy)[0] >= 0] = np.nan
            # z[(xy[0] - 1) ** 3 - xy[1] + 1 >= 0] = np.nan
            # z[xy[0] + xy[1] - 2 >= 0] = np.nan

            plt.figure()
            plt.colorbar(plt.contourf(xx, yy, z, 50, cmap='turbo'))

            plt.xlabel('x')
            plt.ylabel('y')
            plt.plot(min_arg_x1_list,min_arg_x2_list, 'Black')
            plt.plot(min_arg[0], min_arg[1], 'rx', ms=5)

        if self.ARG_NUMBER == 3:
            if len(self.BOUNDS[0]) != 0:
                x = np.linspace(self.BOUNDS[0][0], self.BOUNDS[0][1], 20)
            else:
                x = np.linspace(-5, 5, 20)
            if len(self.BOUNDS[1]) != 0:
                y = np.linspace(self.BOUNDS[1][0], self.BOUNDS[1][1], 20)
            else:
                y = np.linspace(-5, 5, 20)
            if len(self.BOUNDS[2]) != 0:
                z = np.linspace(self.BOUNDS[2][0], self.BOUNDS[2][1], 20)
            else:
                z = np.linspace(-5, 5, 20)

            X, Y, Z = np.meshgrid(x, y, z)

            U = []
            for t in range(len(X)):
                U.append(self.read_function(objective_function, [X[t], Y[t], Z[t]])[0])

            # Creating figure
            plt.figure()
            ax = plt.axes(projection="3d")

            # Creating plot
            plt.colorbar(ax.scatter3D(X, Y, Z, c=U, cmap='turbo', alpha=0.7, marker='.'))
            ax.scatter(min_arg[0], min_arg[1], min_arg[2], 'rx', linewidths=5)
            plt.xlabel('x')
            plt.ylabel('y')

        plt.show()

        return min_val, min_arg
