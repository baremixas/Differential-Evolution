from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QTextEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Slot

from differential_algorithm import DifferentialEvolution


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(1050, 660)
        self.setWindowTitle("Differential Evolution Algorithm")

        # load ui
        loader = QUiLoader()
        self.window = loader.load('ApplicationGUI.ui', self)

        # connect signals
        self.window.calculate.clicked.connect(self.calculate)
        self.window.plot.clicked.connect(self.plot)

        self.window.add_restrict_function.clicked.connect(self.add_restrict)
        self.window.clear_restrict_functions.clicked.connect(self.clear_functions)

        self.window.inequality.clicked.connect(self.change_checkbox_equality)
        self.window.inequality_equality.clicked.connect(self.change_checkbox_inequality_equality)

        self.window.insert_linear_bounds.clicked.connect(self.add_bounds)
        self.window.clear_linear_bounds.clicked.connect(self.clear_bounds)

        # make fields read-only
        self.window.all_restrict_functions.setReadOnly(True)
        self.window.all_restrict_functions_values.setReadOnly(True)
        self.window.all_restrict_functions_inequality.setReadOnly(True)
        self.window.all_linear_bounds.setReadOnly(True)
        self.window.min_value.setReadOnly(True)
        self.window.min_arguments.setReadOnly(True)

        # set initial, required values
        self.window.line_insert_objective_function.setText('x[0] + x[1]')
        self.window.line_insert_linear_bounds.setText('[]')
        self.window.iteration_number.setText('50')
        self.window.population_number.setText('30')
        self.window.CR_var.setText('0.5')
        self.window.F_var.setText('0.5')

        self.differential = DifferentialEvolution()

        self.show()

    @Slot()
    def calculate(self):
        self.window.min_value.clear()
        self.window.min_arguments.clear()

        try:
            self.differential.L = int(self.window.iteration_number.text())
        except:
            print('Wrong number of iterations (has to be int)')

        try:
            self.differential.POPULATION_SIZE = int(self.window.population_number.text())
        except:
            print('Wrong number of population (has to be int)')

        try:
            self.differential.CR = float(self.window.CR_var.text())
        except:
            print('Wrong CR parameter (has to be float [0.0, 1.0])')

        try:
            self.differential.F = float(self.window.F_var.text())
        except:
            print('Wrong F parameter, pick from the list')

        self.differential.ARG_NUMBER = self.window.number_arg.value()
        self.differential.FUNCTION = self.window.line_insert_objective_function.text()

        self.differential.differential_algorithm()

        self.window.min_value.append(str(self.differential.min_val))
        self.window.min_arguments.append(str(self.differential.min_arg))

        if len(self.differential.RESTRICT_FUNCTIONS) != 0:
            for value in self.differential.restrict_functions_values:
                self.window.all_restrict_functions_values.append(str(value))

    @Slot()
    def plot(self):
        self.differential.plot(self.window.trail.isChecked())

    @Slot()
    def add_restrict(self):
        fun = self.window.line_insert_restrict_function.text()

        if fun:
            self.window.all_restrict_functions.append(fun)
            self.differential.RESTRICT_FUNCTIONS.append(fun)

            if self.window.inequality_equality.isChecked():
                self.window.all_restrict_functions_inequality.append('<= 0')
                self.differential.INEQUALITY.append(False)
            elif self.window.inequality.isChecked():
                self.window.all_restrict_functions_inequality.append('< 0')
                self.differential.INEQUALITY.append(True)

    @Slot()
    def add_bounds(self):
        bound = self.window.line_insert_linear_bounds.text()
        self.window.all_linear_bounds.append(bound)

        bound_stripped = bound.strip('][').split(',')

        for element in range(len(bound_stripped)):
            if len(bound_stripped[element]) != 0:
                bound_stripped[element] = float(bound_stripped[element])
            else:
                bound_stripped.pop()

        self.differential.BOUNDS.append(bound_stripped)

    @Slot()
    def clear_bounds(self):
        self.differential.BOUNDS.clear()

    @Slot()
    def clear_functions(self):
        self.differential.RESTRICT_FUNCTIONS.clear()
        self.differential.INEQUALITY.clear()

    @Slot()
    def change_checkbox_inequality_equality(self):
        if self.window.inequality_equality.isChecked():
            self.window.inequality.setChecked(False)
        else:
            self.window.inequality.setChecked(True)

    @Slot()
    def change_checkbox_equality(self):
        if self.window.inequality.isChecked():
            self.window.inequality_equality.setChecked(False)
        else:
            self.window.inequality_equality.setChecked(True)
