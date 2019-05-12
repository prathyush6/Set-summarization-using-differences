import random

n = 10000
m = 10000 #subsets#p = 0.05

fw = open('syn-3', 'w')
covered = set([])
dict_ss = {}
for i in range(0, m):
    p = random.random()/5
    print(p)
    if p < 0.05:
       p = 0.05
    temp = []
    for j in range(1, n+1):
        choice = random.random() < p 
        if choice:
            temp.append(j)
            covered.add(j)
        #print(i, j)
    if len(temp) == 0:
        print("empty set")
    dict_ss[i] = temp
#print(dict_ss)
print("covered "+str(len(covered)))
for k,v in dict_ss.items():
    row = ""
    k = 1
    for j in v:
        if k == len(v):
            row = row + str(j)+"\n"
        else:
            row = row + str(j)+" "
        k = k + 1
    fw.write(row)
fw.close()
