import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QTextEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Slot

import numpy as np
import copy
import matplotlib.pyplot as plt
from math import e, pi

from differential_algorithm import DifferentialEvolution

bounds = []
func_list = []

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


        diff = DifferentialEvolution(function_str, num_arg, bounds, func_list, population_size, L, F, CR)
        min_val, min_arg = diff.differential_algorithm()


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
