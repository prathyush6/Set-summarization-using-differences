#!/usr/bin/python

# Copyright (c) 2018 Prathyush Sambaturu

#Iterated Submodular Set Cover algorithm
import SubModularSetCover

def IteratedSubmodularSetCover(S, T):
    X = [] #X[i]: collection of sets forming solution X
    X.append(set([]))  
  
    #default weight of each set is 1
    w = []
    for i in range(0, len(S)):
        w.append(1)

    #prepare the impure sets and their weights for calls to submodularsetcover function
    Impure = [] #collection of impure sets or S_T as in paper
    wtImpure = [] #weight of each impure set for sending in iterations
    for j1 in range(0, len(S)):
        tempset = S[j1].intersection(T)
        if len(tempset) == 0:
           Impure.append(S[j1])
           wtImpure.append(1)
    #print("Impure sets = "+str(Impure))

    #set weights for each subset S_i \in S as follows: w[i] = f_X0(S_i) = 1+ submodularsetcover(S_T, w, T) 
    for j2 in range(0, len(S)):
        tempComp = S[j2] - T
        if len(tempComp) == 0:
           cov1 = 0
        else:
           selected1, list1 = SubModularSetCover.submodularsetcover(Impure, wtImpure, tempComp)
           cov1 = len(selected1)
        w[j2] = 1 + cov1
    #print("weights of subsets before 1st iteration "+str(w))

    #iterated ssc
    selected2, list2 = SubModularSetCover.submodularsetcover(S, w, T)
    X.append(list2)
    #print(X)
    #print("length of X "+str(len(X[1])))
    #Y = []
    #XUnion = set([])
    #for j in X[1]:
    #    #print(str(S[j])+" \n")
    #    XUnion = XUnion.union(S[j])
    #print("Elements cover by X "+str(XUnion))
    #tempComp3 = XUnion - T
    #print("Unwanted elements : "+str(tempComp3))
    #if len(tempComp3) == 0:
    #   Y = set([])
    #else:
    #   selected6, list6 = SubModularSetCover.submodularsetcover(Impure, wtImpure, tempComp3)
    #   Y = list6
    #print("len of Y "+str(len(Y)))
    #recompute weights of each set for next iteration w[i] = term1 - term2 +term3
    for d in range(1, 4): 
        print("Iteration :"+str(d))
        for i in range(0, len(S)):
            if i in X[d]:
               term3 = 0
            else:
               tempComp1 = S[i] - T
               selected3, list3 = SubModularSetCover.submodularsetcover(Impure, wtImpure, tempComp1)
               cov2 = len(selected3)
               term3 = 1 + cov2
              
            term2 = 0
            XdUnion = set([])
            for l in X[d]:
                XdUnion = XdUnion.union(S[l])
            tempComp4 = XdUnion - T
            cov4 = 0
            if len(tempComp4) != 0:
               selected7, list7 = SubModularSetCover.submodularsetcover(Impure, wtImpure, tempComp4)
               cov4 = len(list7)
            term1 = len(X[d]) + cov4   #f(X^t)


            XtdSi = X[d] - set([i])  #sets in X[d] minus S[i]
            for j in XtdSi:
                XtdSj = X[d] - set([j])
                XtdSjU = set([])
                for l in XtdSj:
                    XtdSjU = XtdSjU.union(S[l])
                tempComp5 = XtdSjU - T
                cov5 = 0
                if len(tempComp5) != 0:
                   selected8, list8 = SubModularSetCover.submodularsetcover(Impure, wtImpure, tempComp5)
                   cov5 = len(list8)
                term2_2 = len(XtdSj) + cov5
                term2 = term2 + term1 - term2_2

            w[i] = term1 -term2 + term3
             
        selected5, list5 = SubModularSetCover.submodularsetcover(S, w, T)
        X.append(list5)
        print(len(X[d+1]))
        if X[d+1] == X[d]:
           print("Convergence ")
           break
        #print("Size of X "+str(len(list5)))
        #print(X[d+1])
       
        Y = []
        XUnion = set([])
        for j in X[d+1]:
             #print(str(S[j])+" \n")
            XUnion = XUnion.union(S[j])
            #print("Elements cover by X "+str(XUnion))
        tempComp3 = XUnion - T
        #print("Unwanted elements : "+str(tempComp3))
        if len(tempComp3) == 0:
           Y = set([])
        else:
           selected6, list6 = SubModularSetCover.submodularsetcover(Impure, wtImpure, tempComp3)
           Y = list6
        print("X length "+str(len(X[d+1])))
        print("Y length "+str(len(Y)))
    
    #find Y
    Y = []
    XUnion = set([])
    for j in X[d+1]:
        #print(str(S[j])+" \n")
        XUnion = XUnion.union(S[j])
    #print("Elements cover by X "+str(XUnion))
    tempComp3 = XUnion - T
    #print("Unwanted elements : "+str(tempComp3))
    if len(tempComp3) == 0:
       Y = set([])
    else:
       selected6, list6 = SubModularSetCover.submodularsetcover(Impure, wtImpure, tempComp3)    
       Y = list6
    #print("Target set size : "+str(len(T)))
    out2 = "Size of X: "+str(len(X[d+1]))+"\nSize of Y: "+str(len(Y))+"\nISSC Objective: "+str(len(X[d+1]) + len(Y))+"\n"
    return out2
 
if __name__ == "__main__":
   U = set([1, 2, 3, 4, 5, 6, 7, 8])
   S = [ set([1, 2, 3]), 
         set([2, 4]),
         set([3, 6]),
         set([2, 5, 8]),
         set([2, 6, 7]),
         set([5, 8]),
         set([1]),
         set([2]),
         set([3]),
         set([4]),
         set([5]),
         set([6]),
         set([7]),
         set([8])
       ]
   w = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
   T = set([1, 2, 3, 5, 6, 8])
   print("U = "+str(U))
   print("S = "+str(S))
   print("T = "+str(T))
  
   IteratedSubmodularSetCover(S, T)
   #SubModularSetCover1.submodularsetcover(Q, w, Y) 
