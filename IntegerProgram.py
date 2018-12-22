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

    return m, x_s, y_s

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



def round_x(x_s, f):
    nx_s = {}
    print(f)
    for k, gv in x_s.items():
        if gv.X >= 1.0 / float(f):
            nx_s[k] = 1
        else:
            nx_s[k] = 0
    return nx_s


EPSILON = 1e-9
def prob_round_y(y_s, f, epsilon, m, n):
    ny_s = {}
    const = 16 * f * epsilon * epsilon
    for k, gv in y_s.items():
        p = const * math.log(m * n * gv.X + EPSILON)
        p = min(1, p)
        choice = random.random() < p
        if choice:
            ny_s[k] = 1
        else:
            ny_s[k] = 0
    return ny_s
