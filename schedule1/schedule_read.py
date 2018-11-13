# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 05:02:49 2018

@author: Rinat Khabibullin
"""

import pandas as pd
import numpy as np

#filename = 'rienm1_100x100x15_schedule.inc'
keywords = ['WELSPECS','COMPDAT','WCONPROD','WCONINJE','TSTEP']
GROUP = 'G1'
DEPTH = '1*'
DIAM = 0.2


class WellParam:
    """
    store all well params at last date in schedule file
    need to get skin for enchancement acounting
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
                print('Warning: ' + key+ 'string has no end character \ ')
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
                w.type = 'PROD'
                continue
            if key == 'WCONINJE':
                w.phase = params[1]
                w.status_work = params[2]
                w.control = params[3]           
                w.lrat = float(params[4])
                w.bhp = float(params[6])
                w.type = 'INJ'
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
            self.wells[wname] = w
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
        l.append('/')
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
        l.append('/')
        return l

    def make_WCONPROD(self, wname, qliq =10, bhp =50, status = 'OPEN', control = 'BHP', pump=0):
        """
        start stop production keyword
        pump - indicate pump type, 
               0 - self flow, 1 - 100-500, 2 -200-500, 3 - 200-1000
        """
        l=[]
        if wname in self.wells:
            w = self.wells[wname]
        else:
            print('well with name '+ wname + ' not found. command ignored')
            return l
            
        # store all data in dict
        w.lrat = qliq
        w.bhp = bhp 
        w.status_work = status
        w.control = control
        l.append('WCONPROD')
        s_wconprod_hints = ("-- name status control orate wrate grate lrate lrateres bhp /" )
        s_wconprod = ("   " + wname + 
                      "    " + status +
                      "  " + control +
                      "           3*          " + str(qliq) +
                      "        1*   " + str(bhp) +
                      " /" )
        l.append(s_wconprod_hints)
        l.append(s_wconprod)
        l.append('/')
        return l
    
    def make_WCONINJE(self, wname, qliq =10, bhp =50, status = 'OPEN', control = 'BHP', pump=0):
        """
        start stop production keyword
        pump - indicate pump type, 
               0 - self flow, 1 - 100-500, 2 -200-500, 3 - 200-1000
        """
        l=[]
        if wname in self.wells:
            w = self.wells[wname]
        else:
            print('well with name '+ wname + ' not found. command ignored')
            return l

        w.lrat = qliq
        w.bhp = bhp
        w.status_work = status
        w.control = control
        l.append('WCONINJE')
        s_wconinje_hints = ("-- name fluid status control lrate lrateres bhp /" )
        s_wconinje = ("   " + wname + '   WATER '
                      " " + status +
                      "  " + control +
                      "     " + str(qliq) +
                      "        1*   " + str(bhp) +
                      " /")
        l.append(s_wconinje_hints)
        l.append(s_wconinje)
        l.append('/')
        return l
    
    def make_TSTEP(self, num = 1, step = 30):
        l =[]
        l.append('TSTEP')
        l.append(' ' + str(num)+'*'+str(step))
        l.append('/')
        return l


class Events:
    """

    """
    def __init__(self, sname):
        self.excel = []
        self.sname = sname
        self.schedule = Schedule(sname)
        self.schedule_new = []
        self.schedule_new.append('------------------------------------ Schedule Section -----------------------------')
        self.schedule_new.append('SCHEDULE')

    def zapusk(self, event):
        wname = event['Название скважины']
        if wname in self.schedule.wells:
            qliq = event['Контроль дебит']
            bhp = event['Контроль Рзаб']
            status = 'OPEN'
            if self.schedule.wells[wname].type == 'PROD':
                if np.isnan(qliq) == True:
                    control = 'BHP'
                    qliq = '1*'
                    if np.isnan(bhp) == True:
                        bhp = 100
                elif np.isnan(bhp) == True:
                    control = 'LRAT'
                    bhp = '1*'
                else:
                    control = 'BHP'
                    bhp = 100
                self.schedule_new.extend(self.schedule.make_WCONPROD(wname, qliq, bhp, status, control))
            else:
                if np.isnan(qliq) == True:
                    control = 'BHP'
                    qliq = '1*'
                    if np.isnan(bhp) == True:
                        bhp = 400
                elif np.isnan(bhp) == True:
                    control = 'RATE'
                    bhp = 400
                else:
                    control = 'BHP'
                    bhp = 400
                self.schedule_new.extend(self.schedule.make_WCONINJE(wname, qliq, bhp, status, control))
        time = float(event['День']) + float(event['Час'])
        if time == 1:
            num = 1
        else:
            num = 3
        step = round(time / num, 2)
        self.schedule_new.extend(self.schedule.make_TSTEP(num, step))
        # else: Почему-то пайчарм ругается здесь
        #    print('Такой скважины нет')
        return

    def ostanovka(self, event):
        wname = event['Название скважины']
        if wname in self.schedule.wells:
            status = 'SHUT'
            if self.schedule.wells[wname].type == 'PROD':
                self.schedule_new.extend(self.schedule.make_WCONPROD(wname, status = status))
            else:
                self.schedule_new.extend(self.schedule.make_WCONINJE(wname, status = status))
        time = float(event['День']) + float(event['Час'])
        if time == 1:
            num = 1
        else:
            num = 3
        step = round(time / num, 2)
        self.schedule_new.extend(self.schedule.make_TSTEP(num, step))
        # else: Почему-то пайчарм ругается здесь
        #   print('Такой скважины нет')
        return

    @staticmethod
    def determine_z(z_m):
        z_range = np.arange(2500, 2575, 5)
        i = 1
        for z in z_range:
            if z_m > z:
                i += 1
            else:
                break
        return i

    def build_well(self,event):
        wname = event['Название скважины']
        x = event['координата i']
        y = event['координата j']
        z1 = self.determine_z(event['перфорация верх, м'])
        z2 = self.determine_z(event['перфорация низ, м'])
        if event['Тип скважины'] == 'Добывающая':
            phase = 'OIL'  # непонятно обязательно ли на нагн ставить воду т.к. это и отдельно при запуске задается
            w = WellParam(wname)
            w.type = 'PROD'
        else:
            phase = 'WATER'
            w = WellParam(wname)
            w.type = 'INJ'
        skin = 1
        status = 'OPEN'
        self.schedule_new.extend(self.schedule.make_WELL(wname, x, y, z1, z2, phase, status, skin))
        self.schedule.wells[wname] = w
        time = float(event['День']) + float(event['Час'])
        if time == 1:
            num = 1
        else:
            num = 3
        step = round(time / num, 2)
        self.schedule_new.extend(self.schedule.make_TSTEP(num, step))
        return

    def read_excel(self, fname):
        excel = pd.read_excel(fname)
        excel.index.names = ['Index']
        excel.columns = list(excel.loc[6])
        excel = excel[excel.index > 6]
        excel = excel.dropna(subset = ['Дата мероприятия'])
        excel = excel.drop(excel[excel['Название команды'] == 'Проверка'].index)
        self.excel = excel

        for event in excel.iterrows():
            if event[1]['Вид мероприятия'] == 'Запуск скважины':
                self.zapusk(event[1])
            elif event[1]['Вид мероприятия'] == 'Остановка скважины':
                self.ostanovka(event[1])
            elif event[1]['Вид мероприятия'] == 'Строительство новой скважины':
                self.build_well(event[1])

        return

a = Events('rienm1_100x100x15_schedule.inc')
a.read_excel('Мероприятия РиЭНМ МАЙ.xlsx')

with open("schedule_new.inc", "w") as file:
    for item in a.schedule_new:
        print(item, file=file)

#w = Schedule(filename)
