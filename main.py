
from Definitions import TrafficData

filenames= ['data.txt', 'output.txt']

def getData(fin, fout):
    input = open(fin, 'r', encoding='utf-16')
    output = open(fout, 'w', encoding='utf-16')


    traficdata=TrafficData(input)



    input.close()


getData(filenames[0], filenames[1])
