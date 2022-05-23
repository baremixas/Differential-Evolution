import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QTextEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Slot

import numpy as np
import copy
import matplotlib.pyplot as plt
from math import e, pi

from func_from_str import func_read
from crossover import crossover
from mutation import mutation

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

# wymiar wektora, liczba iteracji
L = 50
# współczynnik amplifikacji, do mutacji F = 0.4, 0.9, 0.5 [0,2]
F = 0.5
# prawdopodobieństwo do krzyżowania, CR = [0,1]
CR = 0.5
# prawdopodobieństwo mutacji
PM = 0.15

population_size = 30

# number of population element dimension
num_arg = 2

# list of declared restricting functions
func_list = []

# linear bounds
bounds = []


def obj_f(x, function):
    fun = 0

    try:
        fun = eval(function[0])
    except:
        print("Invalid input function: ", function)

    return fun

def init_population():
    population = []
    for i in range(population_size):
        population.append([])
        valid = True
        while valid == True:
            # generating random population elements
            for j in range(num_arg):
                if len(bounds[j]) != 0:
                    population[i].append(float(np.random.uniform(bounds[j][0], bounds[j][1], 1)))
                else:
                    population[i].append(float(np.random.uniform(-5, 5, 1)))

            # checking if generated element is within restricting functions
            if len(func_list) != 0:
                for value in func_read(func_list, population[i]):
                    if value <= 0:
                        valid = False
            else:
                valid = False

            # if it is not within restrictions remove element
            if valid == True:
                population[i] = []
    return population

def diff_alg(function_str, num_arg, L, F, CR, population_size, func_list, bounds):
    loop_iteration = 1

    # initialise random population within the specified bounds
    population = init_population()
    population_H = copy.deepcopy(population)

    obj_fun = [function_str]

    # calculate init fitness for population
    population_fitness = []
    for i in range(len(population)):
        population_fitness.append(func_read(obj_fun,population[i]))

    loop = True

    min_val = population_fitness[0]
    min_arg = population[0]

    while loop == True:
        for i in range(len(population)):
            el_mut = mutation(i, population, num_arg, F, func_list, bounds)
            el_cross = crossover(el_mut, i, population, num_arg, CR, func_list, bounds)

            population_H[i] = el_cross

            if func_read(obj_fun,population_H[i]) < population_fitness[i]:
                population[i] = population_H[i]
                population_fitness[i] = func_read(obj_fun,population_H[i])

            if population_fitness[i] < min_val:
                min_val = population_fitness[i]
                min_arg = population[i]

        population_H = copy.deepcopy(population)

        loop_iteration += 1
        if loop_iteration > L:
            loop = False

    if num_arg == 2:
        if len(bounds[0]) != 0:
            x = np.linspace(bounds[0][0], bounds[0][1], 100)
        else:
            x = np.linspace(-5, 5, 100)
        if len(bounds[1]) != 0:
            y = np.linspace(bounds[1][0], bounds[1][1], 100)
        else:
            y = np.linspace(-5, 5, 100)

        xx, yy = np.meshgrid(x, y)

        xy = [xx, yy]
        z = obj_f(xy, obj_fun)

        plt.figure()
        plt.colorbar(plt.contourf(xx, yy, z, 50, cmap='turbo'))
        plt.plot(min_arg[0], min_arg[1], 'rx', ms=5)
        plt.xlabel('x')
        plt.ylabel('y')

    if num_arg == 3:
        if len(bounds[0]) != 0:
            x = np.linspace(bounds[0][0], bounds[0][1], 20)
        else:
            x = np.linspace(-5, 5, 100)
        if len(bounds[1]) != 0:
            y = np.linspace(bounds[1][0], bounds[1][1], 20)
        else:
            y = np.linspace(-5, 5, 100)
        if len(bounds[2]) != 0:
            z = np.linspace(bounds[2][0], bounds[2][1], 20)
        else:
            z = np.linspace(-5, 5, 100)

        X, Y, Z = np.meshgrid(x, y, z)

        U = []
        for t in range(len(X)):
            U.append(func_read(obj_fun,[X[t], Y[t], Z[t]]))

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


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(1028, 720)
        self.setWindowTitle("Differential Evolution Algorithm")

        # load ui
        loader = QUiLoader()
        self.window = loader.load('ApplicationGUI.ui', self)

        # connect signals
        self.window.calculate.clicked.connect(self.calculate)

        self.window.add_restrict_function.clicked.connect(self.add_restrict)
        self.window.clear_restrict_functions.clicked.connect(self.clear_functions)

        self.window.insert_linear_bounds.clicked.connect(self.add_bounds)
        self.window.clear_linear_bounds.clicked.connect(self.clear_bounds)

        self.window.all_restrict_functions.setReadOnly(True)
        self.window.all_linear_bounds.setReadOnly(True)

        self.show()

    @Slot()
    def calculate(self):
        global num_arg, L, F, CR, population_size, num_arg, func_list, bounds

        self.window.min_value.clear()
        self.window.min_arguments.clear()

        try:
            L = int(self.window.iteration_number.toPlainText())
        except:
            print('Wrong number of iterations (has to be int)')

        try:
            population_size = int(self.window.population_number.toPlainText())
        except:
            print('Wrong number of population (has to be int)')

        try:
            CR = float(self.window.CR_var.text())
        except:
            print('Wrong CR parameter (has to be float [0.0, 1.0])')

        try:
            F = float(self.window.F_var.item(self.window.F_var.currentRow()).text())
        except:
            print('Wrong F parameter, pick from the list')

        num_arg = self.window.number_arg.value()

        function_str = self.window.line_insert_objective_function.text()

        min_val, min_arg = diff_alg(function_str, num_arg, L, F, CR, population_size, func_list, bounds)

        self.window.min_value.append(str(min_val))
        self.window.min_arguments.append(str(min_arg))

    @Slot()
    def add_restrict(self):
        global num_arg, L, F, CR, population_size, num_arg, func_list, bounds

        fun = self.window.line_insert_restrict_function.text()
        self.window.all_restrict_functions.append(fun)

        func_list.append(fun)

    @Slot()
    def add_bounds(self):
        global num_arg, L, F, CR, population_size, num_arg, func_list, bounds

        bound = self.window.line_insert_linear_bounds.text()
        self.window.all_linear_bounds.append(bound)

        bound_stripped = bound.strip('][').split(',')

        for element in range(len(bound_stripped)):
            if len(bound_stripped[element]) != 0:
                bound_stripped[element] = float(bound_stripped[element])
            else:
                bound_stripped.pop()

        bounds.append(bound_stripped)

    @Slot()
    def clear_bounds(self):
        global num_arg, L, F, CR, population_size, num_arg, func_list, bounds

        bounds.clear()

    @Slot()
    def clear_functions(self):
        global num_arg, L, F, CR, population_size, num_arg, func_list, bounds

        func_list.clear()
