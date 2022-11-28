import sys
print(sys.version)
import time
import numpy as np
import matplotlib
import quadprog
from quadprog import solve_qp
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from dynamics import Dyn
from agent import Agent
from obstacle import Sphere, Ellipsoid, Wall
from gurobipy import *
from goal import Goal
from sim_plots import Cbf_data, Clf_data, ColorManager
from params import *
from scipy.sparse import csr_matrix, lil_matrix
import constants as const
import math
import re
import warnings

class QpElement:
    def __init__(self, name, value = 0):
        self.name = name
        self.value = value
        self.modified = True

    def __str__(self):
        return self.name
    
    def __pos__(self):
        return self

    def __neg__(self):
        self.value = -self.value
        return self
    
    def __add__(self, ele):
        # return self.value + ele.value
        return QpExpression(self) + ele

    def __sub__(self, ele):
        return QpExpression(self) - ele

    def __mul__(self, ele):
        return QpExpression(self) * ele

    def __div__(self, ele):
        return QpExpression(self) / ele

    def __le__(self, ele):
        return QpExpression(self) <= ele

    def __ge__(self, ele):
        return QpExpression(self) >= ele

    def __eq__(self, ele):
        return QpExpression(self) == ele

class QpVariable(QpElement):
    def __init__(self, name, lowbound = None, upbound = None, value = 0):
        QpElement.__init__(self, name, value)
        self.name = name
        self.lowbound = lowbound
        self.upbound = upbound
        self.value = value
    
    def ToDict(self):
        return dict(
            name = self.name,
            lowbound = self.lowbound,
            upbound=self.upbound,
            value = self.value,
        )
    



def main():
    a = QpElement('a', 2)
    b = QpElement('b', 3)
    print(a+b)
    c = QpVariable('a','b',value = 3)
    print(c.ToDict())

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print("Total runtime: ", end_time - start_time)