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

    def getLb(self):
        return self.lowbound

    def getUb(self):
        return self.upbound

    def bounds(self, low, up):
        self.lowbound = low
        self.upbound = up
    
class QpExpression:
    def __init__(self, e=None, constant=0, name=None):
        self.name = name
        if e is None:
            e = {}
        if isinstance(e, QpExpression):
            # Will not copy the name
            self.constant = e.constant
            super().__init__(list(e.items()))
        elif isinstance(e, dict):
            self.constant = constant
            super().__init__(list(e.items()))
        elif isinstance(e, QpElement):
            self.constant = 0
            super().__init__([(e, 1)])

    def value(self):
        s = self.constant
        for v, x in self.items():
            if v.varValue is None:
                return None
            s += v.varValue * x
        return s
    
    def copy(self):
        """Make a copy of self except the name which is reset"""
        # Will not copy the name
        return QpExpression(self)
    
    def addterm(self, key, value):
        y = self.get(key, 0)
        if y:
            y += value
            self[key] = y
        else:
            self[key] = value

    def __str__(self, constant=1):
        s = ""
        for v in self.sorted_keys():
            val = self[v]
            if val < 0:
                if s != "":
                    s += " - "
                else:
                    s += "-"
                val = -val
            elif s != "":
                s += " + "
            if val == 1:
                s += str(v)
            else:
                s += str(val) + "*" + str(v)
        if constant:
            if s == "":
                s = str(self.constant)
            else:
                if self.constant < 0:
                    s += " - " + str(-self.constant)
                elif self.constant > 0:
                    s += " + " + str(self.constant)
        elif s == "":
            s = "0"
        return s

    def sorted_keys(self):
        """
        returns the list of keys sorted by name
        """
        result = [(v.name, v) for v in self.keys()]
        result.sort()
        result = [v for _, v in result]
        return result

    def __repr__(self):
        l = [str(self[v]) + "*" + str(v) for v in self.sorted_keys()]
        l.append(str(self.constant))
        s = " + ".join(l)
        return s

    def addInPlace(self, other):
        if isinstance(other, int) and (other == 0):
            return self
        if other is None:
            return self
        if isinstance(other, QpElement):
            self.addterm(other, 1)
        elif isinstance(other, QpExpression):
            self.constant += other.constant
            for v, x in other.items():
                self.addterm(v, x)
        elif isinstance(other, dict):
            for e in other.values():
                self.addInPlace(e)
        else:
            self.constant += other
        return self

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