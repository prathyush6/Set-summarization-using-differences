#!/usr/bin/python
# Copyright (c) 2018 Prathyush Sambaturu
# Program to compute the curvature of a function f: 2^V -> R

import sys
import ReadFile3

U = {1, 2, 3, 4, 5, 6}
S = {1,2}, {2,3,4}, {1,4,5}, {2,6}, {1}, {2}, {3}, {4}, {5}, {6}
T = {2,3}

def computeCurvature(U, S, T):
    #print("U "+str(U))
    #print("S "+str(S))
    #print("T "+str(T))
    noSets = len(S)

    print("\nf(X) = |X| + |\gamma(X) - T|\n")
    Sunion = set([])
    for s in S:
        Sunion = Sunion.union(s) 
  
    f_S = noSets + len(Sunion-T) #since the union of S is equal to T, f(S) = |S|
    #print("f(S) = "+str(f_S))
  
    fdict = {}
    for j in range(0, len(S)):
        fdict[j] = 1+ len(S[j] -T)
    
    #print(fdict)
 
    fSidict = {}
    for j in range(0, noSets):
        Smjunion = set([])
        for k in range(0, noSets):
            if j != k:
               Smjunion = Smjunion.union(S[k])
        
        print(j,k)
        #print(len(Smjunion, Smjunion1)
        fSidict[j] = noSets -1 + len(Smjunion-T)
    #print(fSidict)
    
    minterm = 1.5
    for j in range(0, noSets):
        ratio = 0
        numerator = float(f_S - fSidict[j])
        denominator = float(fdict[j])
        print(j,numerator, denominator)
        if denominator != 0:
           ratio = numerator / denominator
           if ratio < minterm:
              minterm = ratio
    #print(minterm)    
    curvature = 1-minterm
    print("======================")
    print("Curvature "+str(curvature))
        
  

if __name__ == "__main__":
   U, S, T, w = ReadFile3.readfile(sys.argv[1], sys.argv[2]) 
   computeCurvature(U, S, T)
