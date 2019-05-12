#!/usr/bin/python
import gurobipy as grb
import random
from collections import defaultdict
import math
import gzip

def set_summarize_ilp(U, S, T, w):
    """
    Compute the summarization of T using S.
    """
    
    sis = list(range(len(S)))
    i_si = defaultdict(list)
    for si, s in enumerate(S):
        for i in s:
            i_si[i].append(si)
    
    m = grb.Model("set_summarize_ilp")

    # Add varaiables
    x_s = {si: m.addVar(vtype=grb.GRB.BINARY, name=f"x_{si}") for si in sis}
    y_s = {si: m.addVar(vtype=grb.GRB.BINARY, name=f"y_{si}") for si in sis}

    # Add constraints
    for i in T:
        expr = [(1, x_s[si]) for si in i_si[i]]
        expr = grb.LinExpr(expr)
        m.addConstr(expr >= 1, name=f"must_contain:{i}")
        
        expr = [(1, y_s[si]) for si in i_si[i]]
        expr = grb.LinExpr(expr)
        m.addConstr(expr == 0, name=f"must_not_exclude:{i}")
        
    i_si = list(range(len(S)))
    for i in U - T:
        expr_part = [(1, y_s[si]) for si in i_si[i]]
        for si in i_si[i]:
            expr = expr_part + [(-1, x_s[si])]
            expr = grb.LinExpr(expr)
            m.addConstr(expr >= 0, name=f"exclude_if_included:{i}:{si}")
    
    # Add objective
    expr = []
    expr.extend((1, x) for x in x_s.values())
    expr.extend((1, y) for y in y_s.values())
    expr = grb.LinExpr(expr)
    m.setObjective(expr, grb.GRB.MINIMIZE)
    m.write('set_summarize_ilp.lp')   
    return m, x_s, y_s

def pos_summarize_ilp(U, S, T, w):
    """
    Compute the summarization of T using S.
    """

    sis = list(range(len(S)))
    i_si = defaultdict(list)
    for si, s in enumerate(S):
        for i in s:
            i_si[i].append(si)

    m = grb.Model("pos_summarize_ilp")

    # Add varaiables
    x_s = {si: m.addVar(vtype=grb.GRB.BINARY, name=f"x_{si}") for si in sis}
    #y_s = {si: m.addVar(vtype=grb.GRB.BINARY, name=f"y_{si}") for si in sis}

    # Add constraints
    for i in T:
        expr = [(1, x_s[si]) for si in i_si[i]]
        expr = grb.LinExpr(expr)
        m.addConstr(expr >= 1, name=f"must_contain:{i}")

        #expr = [(1, y_s[si]) for si in i_si[i]]
        #expr = grb.LinExpr(expr)
        #m.addConstr(expr == 0, name=f"must_not_exclude:{i}")
    
    #i_si = list(range(len(S)))
    for i in U - T:
        for si in i_si[i]:
            m.addConstr(x_s[si] == 0, name =f"must not containt: {i}: {si}")

    #    for si in i_si[i]:
    #        expr = expr_part + [(-1, x_s[si])]
    #        expr = grb.LinExpr(expr)
    #        m.addConstr(expr >= 0, name=f"exclude_if_included:{i}:{si}")

    # Add objective
    expr = []
    expr.extend((1, x) for x in x_s.values())
    #expr.extend((1, y) for y in y_s.values())
    expr = grb.LinExpr(expr)
    m.setObjective(expr, grb.GRB.MINIMIZE)
    m.write('pos_summarize_ilp.lp')
    return m, x_s

def set_summarize_lprelax(U, S, T, w):
    """
    Compute the summarization of T using S.
    """
    
    sis = list(range(len(S)))
    i_si = defaultdict(list)
    for si, s in enumerate(S):
        for i in s:
            i_si[i].append(si)
    f = max(len(ss) for ss in i_si.values())
    #print(i_si)
    m = grb.Model("set_summarize_ilp")

    # Add varaiables
    x_s = {si: m.addVar(lb=0, ub=1, vtype=grb.GRB.CONTINUOUS, name=f"x_{si}") for si in sis}
    y_s = {si: m.addVar(lb=0, ub=1, vtype=grb.GRB.CONTINUOUS, name=f"y_{si}") for si in sis}

    # Add constraints
    for i in T:
        expr = [(1, x_s[si]) for si in i_si[i]]
        expr = grb.LinExpr(expr)
        m.addConstr(expr >= 1, name=f"must_contain:{i}")

        expr = [(1, y_s[si]) for si in i_si[i]]
        expr = grb.LinExpr(expr)
        m.addConstr(expr == 0, name=f"must_not_exclude:{i}")

    for i in U - T:
        expr_part = [(1, y_s[si]) for si in i_si[i]]
        for si in i_si[i]:
            expr = expr_part + [(-1, x_s[si])]
            expr = grb.LinExpr(expr)
            m.addConstr(expr >= 0, name=f"exclude_if_included:{i}:{si}")

    # Add objective
    expr = []
    expr.extend((1, x) for x in x_s.values())
    expr.extend((1, y) for y in y_s.values())
    expr = grb.LinExpr(expr)
    m.setObjective(expr, grb.GRB.MINIMIZE)
    return m, x_s, y_s, f


#Rounding 1 - theoretical guarantee
def round_x(x_s, f):
    nx_s = {}
    #print(f)
    for k, gv in x_s.items():
        if gv.X >= 1.0 / float(f):
            nx_s[k] = 1
        else:
            enx_s[k] = 0
    return nx_s

#Rounding 2 for x_s
def round1_x(x_s):
    nx_s = {}
    #print(x_s)
    for k, gv in x_s.items():
        #rounding modified here
        choice = random.random() < min(gv.X*5, 1)
        if choice:
           nx_s[k] = 1
        else:
           nx_s[k] = 0
        #print(nx_s[k])
    return nx_s

EPSILON = 1e-9
def prob_round_y(y_s, f, epsilon, m, n):
    ny_s = {}
    const = 16 * f
    itr = 0
    for k, gv in y_s.items():
        #print(itr)
        itr = itr+1
        p = const * math.log(m*n) * gv.X
        p = min(1, p)
        choice = random.random() < p
        if choice:
            ny_s[k] = 1
        else:
            ny_s[k] = 0
    return ny_s

#Rounding 2 y rounding
def prob_round1_y(nx_s, x_s, y_s, U, S, T):
    ny_s = {}
    Tc = U-T
    for k, gv in y_s.items():
        ny_s[k] = 0
    
    i_si = defaultdict(list)
    for si, s in enumerate(S):
        for i in s:
            i_si[i].append(si)

    #print("came here")
    for i in Tc:
        for si1 in i_si[i]:
            if nx_s[si1] == 1:
               for si2 in i_si[i]:
                   if si1 != si2:
                      #print(y_s[si2].X)
                      q = (float) (y_s[si2].X)/x_s[si1].X 
                      choice = random.random() < q
                      if choice:
                         ny_s[si2] = 1
                      else:
                         ny_s[si2] = 0       

    return ny_s
