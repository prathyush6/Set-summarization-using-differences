#!/usr/bin/python

# Copyright (c) Prathyush Sambaturu

# Program to process data files and 
# prepare the collection of 
# subsets, target set, and Universe, 
# with default weight of 1 for each set
from gurobipy import *
import BaselineHeuristic
import IteratedSSC
import IntegerProgram
import ILP
import LP
import sys
import random
import time
from collections import defaultdict

#start_time = time.time()

def readfile(filename, tsize):
    file = open(filename, "r")
    count = 0
    U = set([])  #universe set
    S = []  #collection of subsets
 
    #prepare S from the data file
    for line in file:
        #print("count "+str(count))
        tempSet = set([])
        columns = line.strip().split(" ")
        for i in range(0, len(columns)):
            columns[i] = columns[i].strip()
            tempInt = int(columns[i]) -1
            #tempInt = int(columns[i])
            tempSet.add(int(tempInt))
            if tempInt not in U: 
               U.add(tempInt)
        count = count + 1
        S.append(tempSet)
    
    #for i in range(0, len(U)):
    #    tempSet = set([i])
    #    S.append(tempSet)
    #    count = count + 1
    print("|S| = "+str(count))
    #print(S[2])
    print("|U| = "+str(len(U)))
    T = set([])#T = set([1, 2, 10, 15, 16, 17, 18, 24, 25, 27, 31, 32, 34, 36, 38, 40, 41, 42, 43, 45, 50])
    tsize = int(tsize)
    print("|T|= "+str(tsize))
    #T = S[2]
    #print("|T| = "+str(len(T)))

    #generate target set T as a randomly chosen subset of U
    for i in range(0, tsize):
        temp = random.randint(0, len(U)-1)
        if i == 1:
           T.add(temp)
        else:
           while temp in T:
                 temp = random.randint(0, len(U)-1)
           T.add(temp)
    #T = U
    R = []
    for j in range(0, len(S)):
        #print(S[j])
        if len(S[j].intersection(T))!= 0:
           R.append(S[j])
    print("R initial size "+str(len(R)))
    
    for i in range(0, len(U)):
        tempSet = set([i])
        R.append(tempSet)
        count = count + 1
    print("R final size "+str(len(R)))
       
    #generate target set T as a randomly chosen subset of U
    #for i in range(0, tsize):
    #    temp = random.randint(0, len(U)-1)
    #    if i == 1:
    #       T.add(temp)
    #    else:
    #       while temp in T:
    #             temp = random.randint(0, len(U)-1) 
    #       T.add(temp)
        
    #print("T = "+str(T))
    w = []
    #print("R size "+str(len(R)))
    for i in range(0, count):
        w.append(1)
    #print("w[i] = "+str(w[0])+" for every i" )
    return U, R, T, w

#check feasibility for Rounding 1 with theoretical guarantee: might need to modify it
def feasibleLP(nx_s, ny_s, U, S, T):
    feasible = 1
    tComp = U - T
    for i in tComp:
        for j in range(0, len(S)):
            sum1 = 0
            if (i in S[j]) and (nx_s[j] == 1):
               #sum1 = 0
               for k in range(0, len(S)):
                   if i in S[k]: 
                      sum1 = sum1 + ny_s[k]
               if sum1 < nx_s[j]:
                  feasible = 0
    return feasible    

#check feasibility for Rounding 2 with theoretical guarantee
def feasibleLP1(nx_s, S, T):
    feasible = 1
    #print("came here too")
    #i_si[i] subsets that contain i
    i_si = defaultdict(list)
    for si, s in enumerate(S):
        for i in s:
            i_si[i].append(si)
    for i in T:
        sum_i = 0
        for si in i_si[i]:
            sum_i = sum_i + nx_s[si]
        if sum_i < 1:
           feasible = 0
    #print(feasible)
    return feasible

def objectiveValue(nx_s, ny_s):
    obj = 0
    for i in range(0, len(S)):
        obj = obj + nx_s[i] + ny_s[i]
    return obj

if  __name__ == "__main__":
   fw = open(sys.argv[3],"w")
   gap = float(sys.argv[4])
   start_ip = time.time()
   U, S, T, w = readfile(sys.argv[1], sys.argv[2])
   #print(U)
   #print(T)
   iptime = time.time() - start_ip
   fw.write("Input processing time "+str(iptime)+"\n")
   start_bl = time.time()
   fw.write("===========Baseline Heuristic===========\n")
   out1 = BaselineHeuristic.baselineheuristic(U, S, T) 
   fw.write(out1)
   bltime = time.time() - start_bl
   fw.write("Baseline run time "+str(bltime)+"\n")
   print("baseline completed")  
   
   fw.write("===========ISSC ========================\n")
   start_isc = time.time()
   out2 = IteratedSSC.IteratedSubmodularSetCover(S, T)
   fw.write(out2)
   isctime = time.time() - start_isc
   fw.write("ISSC run time "+str(isctime)+"\n")
   
   fw.write("===========ILP==========================\n")
   start_ilp = time.time()
   m, x_s, y_s = ILP.set_summarize_ilp(U, S, T, w)
   m.setParam(GRB.Param.MIPGap, gap)
   m.optimize() 
   fw.write("ILP Objective value: "+str(m.objVal)+"\n")
   #print(x_s)
   #print(y_s)
   A1 = set([])
   A2 = set([])
   #print("Target Set "+str(T))
   #print("sets in A1")
   #print(S)
   for k, gv in x_s.items():
       if gv.x == 1:
          A1.add(k)
         #print(S[k])
   #print("sets in A2")
   for k, gv in y_s.items():
       if gv.x == 1:
          A2.add(k)
         #print(S[k])
   #print("Sets in positive clause: "+str(A1))
   #print("Sets in negative clause: "+str(A2))
   ilptime = time.time() - start_ilp
   fw.write("ILP run time "+str(ilptime)+"\n")
   
   fw.write("===============LP=========================\n")
   start_lp = time.time()
   mr, xr_s, yr_s, fr = LP.set_summarize_lp(U, S, T, w)  
   mr.optimize()
   lptime = time.time() - start_lp
   #print("LP completed, need to print objective")
   fw.write("LP Objective value: "+str(mr.objVal)+"\n")
   fw.write("LP run time "+str(lptime)+"\n")
   print("end of LP") 
   fw.write("==========Rounding 1======================\n")
   start_r1 = time.time()
   nx_s = IntegerProgram.round_x(xr_s, fr)
   print("Rounded x values in R1")
   #feasible = 0
   #ny_s = IntegerProgram.prob_round_y(yr_s, fr, 0.1, len(S), len(U))
   itr = 0
   minobj = 1000000000
   #print("code was here before rounding 1")
   while itr < 100:
         feasible = 0
         while 1-feasible:
              ny_s = IntegerProgram.prob_round_y(yr_s, fr, 0.1, len(S), len(U))
              #print("Feasibility: "+str(feasibleLP(nx_s, ny_s, U, S, T)))
              feasible = feasibleLP(nx_s, ny_s, U, S, T)
              #print("feasible in R1 "+str(feasible))
         obj = objectiveValue(nx_s, ny_s)
         if obj < minobj:
            minobj = obj
         itr = itr+1
   if minobj > len(T):
      minobj = len(T)
   r1time = time.time() -start_r1 + lptime
   fw.write("LP rounding1 Objective value : "+str(minobj)+"\n")
   fw.write("LP rounding1 runtime "+str(r1time)+"\n")
   #print(nx_s)
   #print(ny_s)
   fw.write("===========Rounding 2====================\n")
   start_r2 = time.time()
   nx_s1 = IntegerProgram.round1_x(xr_s)
   print("Rounding x values in R2")
   feasible = 0
   while 1-feasible:
         nx_s1 = IntegerProgram.round1_x(xr_s)
         feasible = feasibleLP1(nx_s1, S, T)
         #print("feasible "+str(feasible))
   #fw.write("LP rounding2 rounding of x is feasible\n")
      
   itr = 0
   minobj = 1000000000
   while itr < 100:
         feasible = 0
         while 1-feasible:
              ny_s1 = IntegerProgram.prob_round1_y(nx_s1, xr_s, yr_s, U, S, T)
              feasible = feasibleLP(nx_s1, ny_s1, U, S, T)
              #print("feasible "+str(feasible))
         obj = objectiveValue(nx_s1, ny_s1)
         #print("stuck in loop")
         if obj < minobj:
            minobj = obj
         itr = itr+1
   if minobj > len(T):
      minobj = len(T)
   fw.write("LP rounding2 Objective value : "+str(minobj)+"\n")
   r2time = time.time() - start_r2 + lptime
   fw.write("LP rounding2 runtime "+str(r2time)+"\n")
   fw.write("==============END OF RECORD====================\n")

