from pulp import *
import time

def main():
    x_name = ['x_0', 'x_1', 'x_2']
    x = [LpVariable(x_name[i], lowBound = 0, upBound = 10) for i in range(3) ]
    c = LpAffineExpression([ (x[0],1), (x[1],-3), (x[2],4)])
    print(c)

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print("Total runtime: ", (end_time - start_time))


