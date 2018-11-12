# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 18:20:00 2018

@author: Rinat Khabibullin
"""

GROUP = 'G1'
DEPTH = '1*'
DIAM = 0.2
 
def make_WELL(name, x=1,y=1,z1=1,z2=1, phase='OIL', status = 'OPEN', skin = 0):
    """
    make new well keywords 
    """
    l=[]
    l.append('WELSPECS')
    s_welspecs_hints = ("-- name group x y pwf_depth phase /" )
    s_welspecs = ("  " + name + "     " + GROUP +
             "   " + str(x) +
             " " + str(y) +
             " " + str(DEPTH) +
             "        " + str(phase) + " /" )
    l.append(s_welspecs_hints)
    l.append(s_welspecs)
    
    l.append('COMPDAT')
    s_compdat_hints = ("-- name x y z1 z2 perf table  CF  diam KH skin  /" )
    s_compdat = ("   " + name + 
             "   2*   " + str(z1) +
             " " + str(z2) +
             "  " + str(status) +
             "     2*      " + str(DIAM) + 
             "  1*  " + str(skin) + " /" )
    l.append(s_compdat_hints)
    l.append(s_compdat)   
    
    return l

def make_WCONPROD(name, qliq =10, bhp =50, status = 'OPEN', control = 'BHP', pump=0):
    """
    start stop production keyword
    pump - indicate pump type, 
           0 - self flow, 1 - 100-500, 2 -200-500, 3 - 200-1000
    """
    l=[]
    l.append('WCONPROD')
    s_wconprod_hints = ("-- name status control orate wrate grate lrate lrateres bhp /" )
    s_wconprod = ("   " + name + 
                  "    " + status +
                  "  " + control +
                  "           3*          " + str(qliq) +
                  "        1*   " + str(bhp) +
                  " /" )
    l.append(s_wconprod_hints)
    l.append(s_wconprod)
    
    return l

def make_WCONINJE(name, qliq =10, bhp =50, status = 'OPEN', control = 'BHP', pump=0):
    """
    start stop production keyword
    pump - indicate pump type, 
           0 - self flow, 1 - 100-500, 2 -200-500, 3 - 200-1000
    """
    l=[]
    l.append('WCONINJE')
    s_wconinje_hints = ("-- name fluid status control lrate lrateres bhp /" )
    s_wconinje = ("   " + name + '   WATER '
                  " " + status +
                  "  " + control +
                  "     " + str(qliq) +
                  "        1*   " + str(bhp) +
                  " /" )
    l.append(s_wconinje_hints)
    l.append(s_wconinje)
    
    return l

def make_TSTEP(num = 1, step = 30):
    l=[]
    l.append('TSTEP')
    l.append(' ' + str(num)+'*'+str(step))
    l.append('/')
    return l

s1 = make_WELL('P1', skin=10)

for s in s1:
    print(s)
    
s2 = make_WCONPROD('P1')

for s in s2:
    print(s)
    
s3 = make_WCONINJE('I1')
for s in s3:
    print(s)
    
s4 = make_TSTEP(10,1)
for s in s4:
    print(s)
    