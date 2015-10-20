__author__ = 'david_allison'

import time

wonderfullist = [[1,12376763],[2,12366253],[5,123761723]]

duebiouslist = [1,3]

duebiousvalue = 6

timestamp = time.time()

timeint = int(timestamp)

cm = 0

found = 0

while cm < 3:

    if duebiousvalue in wonderfullist[cm]:
        print "List contains", duebiousvalue
        found = 1


    cm = cm + 1

# wonderfullist.append([3,5])

if found == 0 :
    print "Adding ", duebiousvalue, " to list"
    wonderfullist.append([duebiousvalue,timeint])

print wonderfullist