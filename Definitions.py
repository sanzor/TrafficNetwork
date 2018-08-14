from enum import IntEnum
import matplotlib
from matplotlib import pyplot as plt
import itertools
from functools import reduce

goodNodes=[5,6,7,11]
gooddayforNode11="2008-10-26"

class Column(IntEnum):
    ROAD = 0
    SECTION = 1
    FROM = 2
    TO = 3
    TIMESTAMP = 4
    VFLOW=5

class ChartMode(IntEnum):
    IN=0,
    OUT=1,
    DIFF=2



class Results:
    DayData={}

class Data:
    def __init__(self,timeStamp,vehicleFlow,sectionSign):
        self.Timestamp =timeStamp
        if(sectionSign=='1'):
            self.VehicleFlow=int(vehicleFlow[:-1])
        else:
            self.VehicleFlow=(-1)*int(vehicleFlow[:-1])


class Node:
    def __init__(self,_name):
        self.name=_name
        self.IN={}
        self.OUT={}


    def GetDayData(self,date_day="2008-10-23",mode=1):
        daydata = self.selectModeData(mode, date_day)
        hourlyFlow = {}
        hours = set(list(map(lambda pair: self.getTime(pair[0]), daydata)))
        for hour in list(map(lambda elem: (str(elem), '0' + str(elem))[elem < 10], range(0, 24))):
            hourlyFlow[hour] = reduce((lambda flow, nextFlow: flow + nextFlow),
                                      list(map(lambda pair: pair[1], self.getHourlyData(hour, daydata))))
        return hourlyFlow
       # plt.xlabel("Time of day")
        #plt.ylabel("Vehicle Flow")
        #plt.title("Variation for Node: " + self.name + "\nOn day:"+date_day+"\nMode:"+str(ChartMode(mode)) )

    def GetWeekData(self,startdate):


       # plt.plot(hourlyFlow.keys(),hourlyFlow.values())
        #plt.show()

    def getHourlyData(self,hour,dailydata):
        for pair in dailydata:
         targetHourArray=list(filter(lambda pair:self.getHour(self.getTime(pair[0]))==self.getHour(hour),dailydata))
        return targetHourArray



    def getTime(self,fulldate):
        return fulldate.split(' ')[1]

    def getHour(self,Time):
        return Time.split(':')[0]





    def selectModeData(self,mode,date_day):

        if(mode==ChartMode.IN):
            data=[(k,v)for (k,v) in self.IN.items() if k.split(' ')[0]==date_day]
        elif(mode==ChartMode.OUT):
            data=[(k,v) for (k,v) in self.OUT.items() if k.split(' ')[0]==date_day]
        elif(mode==ChartMode.DIFF):
            data=[]
            for (k,v) in self.IN.items():
                if(k.split(' ')[0]==date_day):
                    try:
                        data.append((v,self.OUT[k]))
                    except:
                        data.append((0,0))
        return data



class Pair:
    def __init__(self,To,From):
        self.To=To
        self.From=From
        self.Values=list()



class TrafficData:


    DataMatrix =[[]]
    def __init__(self,file):
       self.initialize(file)

    def initialize(self,file):

        for node in self.getNodes():
            node.GetDayData("2008-10-23",ChartMode.IN)
        print("Sugi pwla")

    def getNodes(self,file):
        self.DataMatrix = [[word for word in line.split('\t')] for line in file.readlines()[1:] if
                           len(line.split('\t')) > 5]
        self.nodes = list(
            map(lambda nodename: Node(nodename), set(self.getColumn(Column.TO) + self.getColumn(Column.FROM))))
        self.Pairs = self.getPairData()
        for node in self.nodes:
            for pair in self.Pairs.values():
                if (node.name in [pair.To, pair.From]):
                    self.insertGroupInNode(node, pair)

        return list(filter(lambda node: len(node.IN) > 0 and len(node.OUT) > 0, self.nodes))

    def insertGroupInNode(self,node,pair):
        for sample in pair.Values:
            if(node.name==pair.To and sample.VehicleFlow>0):
                if(sample.Timestamp not in node.IN.keys()):
                    node.IN[sample.Timestamp]=0
                node.IN[sample.Timestamp]+=sample.VehicleFlow
            elif(node.name==pair.From and sample.VehicleFlow<0):
                 if(sample.Timestamp not in node.OUT.keys()):
                     node.OUT[sample.Timestamp]=0
                 node.OUT[sample.Timestamp]+=(-1)*sample.VehicleFlow





    def getPairData(self):
        Pairs={}
        for line in self.DataMatrix:
            if (line[Column.TO], line[Column.FROM]) not in Pairs.keys():
                Pairs[(line[Column.TO],line[Column.FROM])]=Pair(line[Column.TO],line[Column.FROM])

            Pairs[(line[Column.TO],line[Column.FROM])].Values.append(Data(line[Column.TIMESTAMP],line[Column.VFLOW],(line[Column.SECTION])[-1]))
        return Pairs


    def getColumn(self,columnName):
        return [line[columnName] for line in self.DataMatrix]





