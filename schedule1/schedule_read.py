# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 05:02:49 2018

@author: Rinat Khabibullin
"""

filename = 'rienm1_100x100x15_schedule.inc'
keywords =['WELSPECS','COMPDAT','WCONPROD','WCONINJE','TSTEP']
GROUP = 'G1'
DEPTH = '1*'
DIAM = 0.2

class WellParam:
    """
    store all well params at last date in schedule file
    need to get skin for  enchancement acounting 
    """
    def __init__(self,name,x=1,y=1,z1=1,z2=1):
        self.x = x
        self.y = y
        self.z1 = z1
        self.z2 = z2
        self.group = GROUP
        self.phase = "OIL"
        self.type = 'PROD'
        self.status_perf = "OPEN"
        self.status_work = 'OPEN'
        self.kh = "1*"
        self.skin = 0
        self.diam = DIAM
        self.cf = "1*"
        self.filttablenum = "1*"
        self.depth = "1*"
        self.lrat = 10
        self.bhp = 50
        self.control = 'BHP'


class Schedule:
    """
    schcedule reader and parser
    generate list (dicr) of wells in schedule file with params at last date
    """
    def __init__(self, fname):
        self.keys = []
        self.lastkey = []
        self.wells = {}             # well dict
        self.read_file(fname)       # read and parse file
        for l in self.keys:
            self.read_key(l[0],l)   # read keys and params
            
    
    def read_file(self, name):
        """
        read file 
        break all file content into keywords for further analysis
        """
        try:
            file = open(name)
        except:
            print('error reading file ' + name)
            return
        # delete leading and trailing spaces and \n from file
        self.content = [line.rstrip('\n') for line in file]
        self.content = [line.strip() for line in self.content]
        keyread = False
        for line in self.content:
            if line[:2] == '--':            # comment in file detected
                continue
            if line == 'SCHEDULE':          # section title ignored 
                print('SCHEDULE section detected')
                continue
            if line in keywords:            # looking only keywords of interest
                print('keyword '+ line +' detected')
                self.lastkey = []           # start collecting keyword params
                self.lastkey.append(line)
                keyread = True
                continue     
            if line == '/':                 # end of keyword found
                if keyread:                 # stop collecting if started before
                    self.keys.append(self.lastkey)
                keyread = False
                continue
            if keyread: 
                line=line.replace('2*',' 1* 1* ')
                line=line.replace('3*',' 1* 1* 1* ')
                if len(line) > 2:           # ignore short lines (blank lines)
                    self.lastkey.append(line)
        if keyread:
            self.keys.append(self.lastkey)
            
        print('reading '+name+' done: ' +str(len(self.keys)) +' keywords detected')
        pass


    def read_key(self, key, lines):
        """
        read params from keywords
        store in wells dictionary 
        """
        if lines[0] != key :
            s = 'error parsing ' +key+ '. No ' +key+ ' keyword'
            print(s)
            return s
        for line in lines: 
            if line == key:
                continue
            if len(line) < 2:
                continue
            if key == 'TSTEP':      #ignored at the moment 
                continue
            if line[-1:] != '/':
                print('Warning: ' +key+ 'string has no end character \ ')
            line = line.split('/')[0]
            params = line.split()   # split data line into parama
            wellname = params[0]    # first in line is well name
            if wellname in self.wells:   
                w = self.wells[wellname]
            else:
                w = WellParam(wellname)
                self.wells[wellname] = w
            if key == 'COMPDAT':
                w.z1 = int(params[3])
                w.z2 = int(params[4])
                w.status_perf = params[5]
                w.diam = params[8]
                w.skin = float(params[10])
                continue
            if key == 'WCONPROD':
                w.status_work = params[1]
                w.control = params[2]           
                w.lrat = float(params[6])
                w.bhp = float(params[8])
                continue
            if key == 'WCONINJE':
                w.phase = params[1]
                w.status_work = params[2]
                w.control = params[3]           
                w.lrat = float(params[4])
                w.bhp = float(params[6])
                continue
            if key == 'WELSPECS':
                w.group = params[1]
                w.x = params[2]
                w.y = params[3]
                continue
            print(key + ' param left unread ')
        print(key + ' read done')


    def make_WELL(self, wname, x=1,y=1,z1=1,z2=1, phase='OIL', status = 'OPEN', skin = 0):
        """
        make new well keywords 
        adds new well's data into dict
        """
        l=[]
        if wname in self.wells:
            w = self.wells[wname]
            print('well with name '+ wname + ' already exist. command ignored')
            return l
        else:
            w = WellParam(wname)
        # store all data in dict
        w.x = x
        w.y = y 
        w.z1 = z1
        w.z2 = z2
        w.phase = phase
        w.status_perf = status 
        w.skin = skin
        # generate keywors       
        l.append('WELSPECS')
        s_welspecs_hints = ("-- name group x y pwf_depth phase /" )
        s_welspecs = ("  " + wname + "     " + GROUP +
                 "   " + str(x) +
                 " " + str(y) +
                 " " + str(DEPTH) +
                 "        " + str(phase) + " /" )
        l.append(s_welspecs_hints)
        l.append(s_welspecs)
        
        l.append('COMPDAT')
        s_compdat_hints = ("-- name x y z1 z2 perf table  CF  diam KH skin  /" )
        s_compdat = ("   " + wname + 
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
            
            
w = Schedule(filename)


        

    
