#!/usr/bin/python

# Greedy algorithm for the submodular set cover

#copyright (c) 2018 Prathyush Sambaturu

import priorityqueue

MAXPRIORITY = 9999999

#Input: Collection of subsets Q, weight vector w, target set T

def submodularsetcover(Q, w, T):
    if len(Q) == 0 or len(T) == 0:
       return [], 0
    
    C = set() #elements of T covered so far
    A = list() #sets added to solution
    A_id = set() #set ids added to solution

    Q1 = [] #a copy of Q
    
    for index, item in enumerate(Q):
        Q1.append(set(item))

    alpha = priorityqueue.PriorityQueue()

     
    for i in range(len(Q)):
        a = w[i]
        b = len(T.intersection(Q[i]))
   
        if b == 0:
           alpha.addtask(i, MAXPRIORITY)
        else:
           val = a/float(b)
           alpha.addtask(i, val)

    cost = 0
    #print(T)
    while(len(T) > 0):
          #print(len(T))
          choice = alpha.poptask()
          A.append(Q[choice])
          A_id.add(choice)


          cost = cost + w[choice] 
          C = C.union(Q[choice])

          T = T - C
          for i in range(0, len(Q)):
              a = w[i]
              Q1[i] = Q1[i] - C
              b = len(T.intersection(Q1[i]))
              if b == 0:
                 alpha.addtask(i, MAXPRIORITY)
              else:
                 val = a/float(b)
                 alpha.addtask(i,val)
          #print("target "+str(T))
          #print("Q1 "+str(Q1))
          #print("I'm here")
    return A, A_id 

    



if __name__ == "__main__":
   U = set([1,2,3,4,5,6,7,8]) 
   Q = [ set([1,2,3]),
         set([2,3]),
         set([3,4,7]),
         set([3,6,8]),
         set([1,4,5]),
         set([2,3,6,7]),
       ]
   w = [2,3,5,6,1,3]
   T = set([1,2,5,8])
   A, cost = submodularsetcover(Q, w, T)
   print(A)
#print(cost)
