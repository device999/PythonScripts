import json
from pprint import pprint
import math

with open('dataPart2.json') as data_file:    
    data = json.load(data_file)
#pprint(data[2]['city'])
for i in xrange(len(data)):
    if data[i]!=None and data[i]['founded']>1950:
        print data[i]['founded']
print "---------------------------------------------------"
counter = 0
mylist=[]
for i in xrange(len(data)):
    if data[i]==None:
        mylist.append(i)

for z in xrange(len(mylist)):
    data.pop(mylist[z]-z)
years=[]
for i in xrange(len(data)):
    if data[i]['size']=="11-50 employees" or data[i]['size']=="1-10 employees":
        print data[i]['size']
    else:
        years.append(i)
print years
for z in xrange(len(years)):
    data.pop(years[z]-z)
f = open('resultsPart2.json', 'w')
json.dump(data, f, indent=4)
           

