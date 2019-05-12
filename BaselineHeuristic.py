#!/usr/bin/python

# Copyright (c) 2018 Prathyush Sambaturu

# Baseline heuristic for the Set Summarization Problem (SSP)

import SubModularSetCover
  

def baselineheuristic(U, S, T):
  pure = [] #list of pure sets
  impure = [] #list of impure sets
  mixed = [] #list of mixed sets
  puremixed = [] #pure mixed sets
  PureMixed =  [] #pure and mixed sets
  wtPureMixed = [] #weights of pure mixed
  w = [] # cost of sets

  Impure = [] #collection of impure sets
  wtImpure = [] #weight of each impure set for sending in iterations
 
  #print("entered here-1")
  for i in range(0, len(S)):
      tempset = S[i].intersection(T)
      if len(tempset) == 0:
         #print(str(S[i])+" is an impure set")
         impure.append(i)
         Impure.append(S[i])
         wtImpure.append(1)
         w.append(len(S[i]))
      elif S[i] == tempset:
         pure.append(i)
         puremixed.append(i)
         PureMixed.append(S[i])
         w.append(1)
         wtPureMixed.append(1)
   
      else:
         mixed.append(i)
         puremixed.append(i)
         PureMixed.append(S[i])
         w.append(1)
         wtPureMixed.append(1)

  #print(PureMixed)
  #print(str(len(impure)))
  #print(Impure)
  #print(wtImpure)
 
  #impure sets weights
  #print("entered here 2 "+str(len(impure)))
  count = 0
  for index, item in enumerate(impure):  
      tempImpure = []
      tempWtImpure = []
      intCurr = 0 #no of items in intersection b/w current impure set and other impure sets
      #print("inside loop after 2")
      for index1, item1 in enumerate(impure):
          #print("stuck up here"+str(index1))
          if item1 != item:  
             tempImpure.append(S[item1])
             tempWtImpure.append(1)
             intCurr = len(S[item1].intersection(S[item])) + intCurr
     
      if intCurr != 0:
         count = count+1
         selected, cost = SubModularSetCover.submodularsetcover(tempImpure, tempWtImpure, S[item])
         #print("done here 2 "+ str(count))
         if w[item] > len(selected):
            w[item] = len(selected)

  #print("entered here 3 "+str(len(mixed)))
  count = 0
  #mixed sets weights
  for index2, item2 in enumerate(mixed):
      count = count + 1
      diff = U - T
      tempComp = S[item2].intersection(diff)
      if len(tempComp) == 0: 
         cov = 0
      else:
         selected, cost = SubModularSetCover.submodularsetcover(Impure, wtImpure, tempComp)
         cov = len(selected)
      w[item2] = 1+len(selected) 
      #print("done here 3 "+str(count))
     
  #print("entered here 4 "+str(len(puremixed)))
  #pureMixed set weights
  
  for index3, item3 in enumerate(puremixed): 
      wtPureMixed[index3] = w[item3]
  #print("Pure Mixed "+str(PureMixed))
  #print(wtPureMixed)
  
  #print("entered here 5")
  #Compute A1 consisting only of pure and mixed subsets in S 
  A1, cost = SubModularSetCover.submodularsetcover(PureMixed, wtPureMixed, T)
  #print("Sets selected for A1: \n")
  #for i in A1:
  #    print(str(sorted(i))+"\n")
  #print("I came here")
  A1elements = set([])
  for i in range(0, len(A1)):
      A1elements = A1elements.union(A1[i])
  #print("union of all elements in A1: "+str(A1elements))
  #print("Target set "+str(T))
  #set of elements to be eliminated
  W = A1elements - T
  #print("unwanted elements to be removed: "+str(W)) 
  if len(W) != 0:
     #make weight of each impure set 1
     for index, item in enumerate(impure):
         wtImpure[index] = 1
     #print("Modified wtImpure "+str(wtImpure))
 
     #print("Impure Sets : \n")
     #print(Impure) 
     # find collection A2, subset of Impure, such that W is covered with minimum cost
     A2, cost = SubModularSetCover.submodularsetcover(Impure, wtImpure, W)
  else:
     A2 = set([])
  #print("Sets selected for A2 \n")
  #for i in A2:
  #   print(str(sorted(i))+"\n")   
  
  A2elements = set([])
  for j in range(0, len(A2)):
      A2elements = A2elements.union(A2[j])
  finalT = A1elements - A2elements
  #print("Initial T: "+str(T))
  #print("Our representation : "+str(finalT))
  print("==========================")
  #fw = open("ts_op", "w") 
  out1 = "Size of X: "+str(len(A1))+"\n"+"Size of Y: "+str(len(A2))+"\nBaseline Objective  : "+str(len(A1) + len(A2))+"\n"

  return out1

if __name__ == "__main__":
  #baselineheuristic()
  U = set([1, 2, 3, 4, 5, 6, 7, 8])  #universe set
  S = [ set([1, 2, 3]),            #set of subsets
        set([2, 3]),
        set([4, 7]),
        set([3, 6, 8]),
        set([1, 5]),
        set([2, 3, 6, 7]),
        set([1]),
        set([2]),
        set([3]),
        set([4]),
        set([5]),
        set([6]),
        set([7]),
        set([8])
      ]
   #w = [2, 3, 5, 6, 1, 3] #weights of sets in Q
  T = set([1, 2, 5, 8])
  print("Universe, U: "+str(U))
  print("Collection of sets, Q: "+str(S))
  #print("weighs of sets in collection, w: "+str(w))
  print("Target Set, Y: "+str(T))
  baselineheuristic(U, S, T)

