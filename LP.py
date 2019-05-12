from gurobipy import *
#import gurobi as grb

from collections import defaultdict

U = {1,2,3,4,5,6}
S = [{1,3,5}, {1,4}, {2,4,6}, {1,2,5,6}, {3,5}, {1,2,5}, {1}, {2}, {3}, {4}, {5}, {6}]
T = {1,3}
w = {1,1,1,1,1,1}
def set_summarize_lp(U, S, T, w):
    m = Model("set_summarization")
    
    sis = list(range(len(S)))
    #x(s), y(s) variables
    xs = {}
    ys = {}
    for j in sis:
        xs[j] = m.addVar(lb = 0, ub = 1, vtype = GRB.CONTINUOUS, name = "xs("+str(j)+")")
        ys[j] = m.addVar(lb = 0, ub = 1, vtype = GRB.CONTINUOUS, name = "ys("+str(j)+")")
   
    #sets that contain i
    i_si = defaultdict(list)
    for si, s in enumerate(S):
        for i in s:
            i_si[i].append(si)     
  
    f = max(len(ss) for ss in i_si.values())
    #print(i_si)
    print("v/f = "+str(f))
    #coverage constraint
    for i in T:
        m.addConstr(quicksum(xs[si] for si in i_si[i]) >= 1, name = "C1("+str(i)+")") 
        #elements in T should not appear in the sets selected for Y
        for si in i_si[i]:
            m.addConstr(ys[si] == 0, name = "C2("+str(i)+","+str(si)+")")
   
    Tc = U.difference(T)
    i_si_nt = []
    #sets that do not have any target set elements
    for j in i_si:
        inter = S[j-1].intersection(T)
        if len(inter) != 0:
           i_si_nt.append(j-1)
    
    #element i in target set and sets that contain i 
    for i in Tc:
        temp = set(i_si[i]) - set(i_si_nt)
        for si in i_si[i]:
            st = set([])
            st.add(si)
            temp1 = set(temp) - set(st)
            m.addConstr( quicksum( ys[k] for k in temp1 ) - xs[si] >= 0, name = "C3("+str(i)+","+str(si)+")")
   
    m.setObjective( quicksum(xs[i]+ys[i] for i in range(0, len(S))), GRB.MINIMIZE)    
    m.update()
    m.write('set_summarization_lp.lp')
    print("Finished generating LP program")
    #m.write('set_summarization.lp')
    return m, xs, ys, f

if __name__== "__main__":
   set_summarize_lp(U, S, T, w)
