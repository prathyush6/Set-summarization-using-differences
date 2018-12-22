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
import sys
import random
import time

start_time = time.time()

def readfile(filename, tsize):
    file = open(filename, "r")
    count = 0
    U = set()  #universe set
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
    
    for i in range(0, len(U)):
        tempSet = set([i])
        S.append(tempSet)
        count = count + 1
    print("|S| = "+str(count))
    print("U = "+str(U))
    T = set([])#T = set([1, 2, 10, 15, 16, 17, 18, 24, 25, 27, 31, 32, 34, 36, 38, 40, 41, 42, 43, 45, 50])
    tsize = int(tsize)
    print("|T|= "+str(tsize))
    
    #generate target set T as a randomly chosen subset of U
    for i in range(0, tsize):
        temp = random.randint(0, len(U)-1)
        if i == 1:
           T.add(temp)
        else:
           while temp in T:
                 temp = random.randint(0, len(U)-1) 
           T.add(temp)
        
    print("T = "+str(T))
    w = []

    for i in range(0, count):
        w.append(1)
    print("w[i] = "+str(w[0])+" for every i" )
    return U, S, T, w

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

def objectiveValue(nx_s, ny_s):
    obj = 0
    for i in range(0, len(S)):
        obj = obj + nx_s[i] + ny_s[i]
    return obj

if  __name__ == "__main__":
   fw = open(sys.argv[3],"w")
   U, S, T, w = readfile(sys.argv[1], sys.argv[2])
   time1 = time.time() - start_time
   fw.write("Input processing time "+str(time1)+"\n")
   fw.write("===========Baseline Heuristic===========\n")
   out1 = BaselineHeuristic.baselineheuristic(U, S, T) 
   time2 = time.time() - start_time
   time3 = time2 - time1
   fw.write(out1)
   fw.write("Baseline run time "+str(time2)+"\n")
   fw.write("===========ISSC ========================\n")
   out2 = IteratedSSC.IteratedSubmodularSetCover(S, T)
   fw.write(out2)
   time4 = time.time() - start_time - time3
   time5 = time4 - time3
   fw.write("ISSC run time "+str(time4)+"\n")
   #fw.write("===========ILP==========================\n")
   #m, x_s, y_s = IntegerProgram.set_summarize_ilp(U, S, T, w)
   #m.optimize() 
   #time6 = time.time() - start_time - time5
   #fw.write("ILP Objective value: "+str(m.objVal)+"\n")
   #fw.write("ILP run time "+str(time6)+"\n")
   #print(x_s)
   #print(y_s)
   #A1 = set([])
   #A2 = set([])
   #print("Target Set "+str(T))
   #print("sets in A1")
   #print(S)
   #for k, gv in x_s.items():
   #    if gv.x == 1:
   #       A1.add(k)
   #       print(S[k])
   #print("sets in A2")
   #for k, gv in y_s.items():
   #    if gv.x == 1:
   #       A2.add(k)
   #       print(S[k])
   #print("Sets in positive clause: "+str(A1))
   #print("Sets in negative clause: "+str(A2))
   #fw.write("===============LP=========================\n")
   #mr, xr_s, yr_s, fr = IntegerProgram.set_summarize_lprelax(U, S, T, w)  
   #mr.optimize()
   #time7 = time.time() - start_time - time5
   #fw.write("LP Objective value: "+str(mr.objVal)+"\n")
   #fw.write("LP run time "+str(time7)+"\n")
   #nx_s = IntegerProgram.round_x(xr_s, fr)
   #feasible = 0
   #ny_s = IntegerProgram.prob_round_y(yr_s, fr, 0.1, len(S), len(U))
   #while 1-feasible:
   #      ny_s = IntegerProgram.prob_round_y(yr_s, fr, 0.1, len(S), len(U))
   #      print("Feasibility: "+str(feasibleLP(nx_s, ny_s, U, S, T)))
   #      feasible = feasibleLP(nx_s, ny_s, U, S, T)
   #obj = objectiveValue(nx_s, ny_s)
   #print("Objective value : "+str(obj))
   #print(nx_s)
   #print(ny_s)
   
