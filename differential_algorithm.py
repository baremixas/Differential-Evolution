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
        self.INEQUALITY = []

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
            for i, value in enumerate(self.read_function(self.RESTRICT_FUNCTIONS, element)):
                if self.INEQUALITY[i]:
                    if value >= 0:
                        valid = False
                else:
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

        self.objective_function = [self.FUNCTION]

        # Calculate init fitness for population
        population_fitness = []
        for i in range(len(self.population)):
            population_fitness.append(self.read_function(self.objective_function, self.population[i])[0])

        loop = True
        loop_iteration = 0

        self.min_val = population_fitness[0]
        self.min_arg = self.population[0]

        # # variables used to test best values configuration
        # self.min_arg_x1_list = []
        # self.min_arg_x2_list = []
        # self.min_val_vec = []
        # self.min_ite_vec = []

        while loop == True:
            for i in range(len(self.population)):
                el_mut = self.mutation(i)
                el_cross = self.crossover(el_mut, i)

                if self.read_function(self.objective_function, el_cross)[0] < population_fitness[i]:
                    self.population[i] = el_cross
                    population_fitness[i] = self.read_function(self.objective_function, el_cross)[0]

                if population_fitness[i] < self.min_val:
                    self.min_val = population_fitness[i]
                    self.min_arg = self.population[i]
                    # self.min_val_vec.append(self.min_val)
                    # self.min_ite_vec.append(loop_iteration)
                    # self.min_arg_x1_list.append(self.min_arg[0])
                    # self.min_arg_x2_list.append(self.min_arg[1])

            loop_iteration += 1
            if loop_iteration >= self.L:
                loop = False

        if len(self.RESTRICT_FUNCTIONS) != 0:
            self.calculate_restrict_functions()

        # # Check for first min iteration
        # for i, value in enumerate(self.min_val_vec):
        #     if abs(value - self.min_val_vec[-1]) < 0.000001:
        #         print(self.min_ite_vec[i])
        #         return

    def calculate_restrict_functions(self):
        self.restrict_functions_values = self.read_function(self.RESTRICT_FUNCTIONS, self.min_arg)

    def plot(self, trail=False):
        if self.ARG_NUMBER == 2:
            if len(self.BOUNDS[0]) != 0:
                x = np.linspace(self.BOUNDS[0][0], self.BOUNDS[0][1], 500)
            else:
                x = np.linspace(-5, 5, 500)
            if len(self.BOUNDS[1]) != 0:
                y = np.linspace(self.BOUNDS[1][0], self.BOUNDS[1][1], 500)
            else:
                y = np.linspace(-5, 5, 500)

            xx, yy = np.meshgrid(x, y)

            xy = [xx, yy]
            z = self.read_function(self.objective_function, xy)[0]

            for restrict in self.RESTRICT_FUNCTIONS:
                z[self.read_function([restrict], xy)[0] >= 0] = np.nan

            plt.figure()
            plt.colorbar(plt.contourf(xx, yy, z, 50, cmap='turbo'))

            plt.xlabel('x')
            plt.ylabel('y')

            if trail:
                plt.plot(self.min_arg_x1_list, self.min_arg_x2_list, 'Black')

            plt.plot(self.min_arg[0], self.min_arg[1], 'rx', ms=5)

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
                U.append(self.read_function(self.objective_function, [X[t], Y[t], Z[t]])[0])

            # Creating figure
            plt.figure()
            ax = plt.axes(projection="3d")

            # Creating plot
            plt.colorbar(ax.scatter3D(X, Y, Z, c=U, cmap='turbo', alpha=0.7, marker='.'))
            ax.scatter(self.min_arg[0], self.min_arg[1], self.min_arg[2], edgecolor='red', linewidths=5)
            plt.xlabel('x')
            plt.ylabel('y')

        plt.show()

