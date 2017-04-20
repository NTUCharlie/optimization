import time
import random
import math

people = [('Seymour','BOS'),
          ('Franny', 'DAL'),
          ('Zooey','CAK'),
          ('Walt','MIA'),
          ('Buddy','ORD'),
          ('Les','OMA')]
detination='LGA'

flights={}
with open('schedule.txt', 'r') as file:
    lines = file.readlines()
    print(lines)
    for i in range(5):
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