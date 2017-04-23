import time
import random
import math

people = [('Seymour','BOS'),
          ('Franny', 'DAL'),
          ('Zooey','CAK'),
          ('Walt','MIA'),
          ('Buddy','ORD'),
          ('Les','OMA')]
destination='LGA'

flights={}
with open('schedule.txt', 'r') as file:
    lines = file.readlines()
    for i in range(len(lines)):
        origin=lines[i].strip().split(',')[0]
        dest = lines[i].strip().split(',')[1]
        depart=lines[i].strip().split(',')[2]
        arrive=lines[i].strip().split(',')[3]
        price=lines[i].strip().split(',')[4]
        flights.setdefault((origin,dest),[])
        flights[(origin,dest)].append((depart,arrive,int(price)))
def getminutes(t):
    x=time.strptime(t,'%H:%M')
    return x[3]*60+x[4]

def printschedule(r):
    for d in range(int(len(r)/2)):
        name=people[d][0]
        origin=people[d][1]
        out=flights[(origin, destination)][r[d]]
        ret=flights[(destination,origin)][r[d+1]]
        print('{} {} {}-{} ${} {}-{} ${}\n'.format(name,origin,out[0],out[1],out[2],ret[0],ret[1],ret[2]))

def schedulecost(sol):
    totalprice=0
    latestarrival=0
    earliestdep=24*60
    for d in range(int(len(sol)/2)):
        origin=people[d][1]
        outbound=flights[(origin,destination)][int(sol[d])]
        returnf=flights[(destination,origin)][int(sol[d+1])]
        totalprice+=outbound[2]
        totalprice+=returnf[2]
        if latestarrival<getminutes(outbound[1]):latestarrival=getminutes(outbound[1])
        if earliestdep>getminutes(returnf[0]):earliestdep=getminutes(returnf[0])

    totalwait=0
    for d in range(int(len(sol)/2)):
        origin=people[d][1]
        outbound=flights[(origin,destination)][int(sol[d])]
        returnf=flights[(destination,origin)][int(sol[d+1])]
        totalwait+=latestarrival-getminutes(outbound[1])
        totalwait+=getminutes(returnf[0])-earliestdep
    if latestarrival>earliestdep:totalprice+=50

    return totalprice+totalwait

def randomoptimize(domain,costf):
    best=999999999
    bestr=None
    for i in range(1000):
        r=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
        cost=costf(r)
        if cost<best:
            best=cost
            bestr=r
    return r

def hillclimb(costf):
    #sol=[random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
    sol=[random.randint(0,8) for i in range(8)]
    print(sol)
    while 1:
        neighbors=[]
        #for j in range(len(domain)):
           # if sol[j]>domain[j][0]:
                #neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
                #print(neighbors)
            #if sol[j]<domain[j][1]:
                #neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
        for i in range(8):
            if sol[i]>0 and sol[i]<8:
                neighbors.append(sol[0:i]+[sol[i]+1]+sol[i+1:])
                print(neighbors)
                neighbors.append(sol[0:i]+[sol[i]-1]+sol[i+1:])
                print(neighbors)
        current=costf(sol)
        print(current)
        best=current
        for j in range(len(neighbors)):
            cost=costf(neighbors[j])
            if cost<best:
                best=cost
                sol=neighbors[j]
        break
    return sol

h=hillclimb(schedulecost)
print(schedulecost(h))
printschedule(h)

