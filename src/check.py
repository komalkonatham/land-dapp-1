import random

def arraytopoly(a = [1,2,3,4]):
    r=[]
    
    for i in range(len(a)):
        b={}
        if(i%2 == 1):
            continue
        b["lat"] = a[i]
        b["lng"] = a[i+1]
        r.append(b)
    return r
r = arraytopoly()
print(r)
        