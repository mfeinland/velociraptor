from asyncio.windows_events import NULL
from asyncore import write
import sys, re
import math
#   command line args
#   1) input UI file path
#   2) input file resolution in the form <WIDTH>x<HEIGHT>
#   3) output file desired resolution in the form <WIDTH>x<HEIGHT>
#   4) output UI file path
#
#   The program automatically calculates the scale factors of the width and height. 
#   To enable font point size scaling, comment out the "NO FONT SCALE" regex expression and uncomment the "FONT SCALE" regex expression

class worker():
    def __init__(self,val):
        # Changed by Santiago to not use command line arguments in July 2023
        #declare command line arguments 
        try:
            # self.inPath = argv[1]
            # self.inRes = argv[2]
            # self.outRes = argv[3]
            # self.outPath = argv[4]
            self.inPath =val[0]
            self.inRes = val[1]
            self.outRes = val[2]
            self.outPath = val[3]
        except:
            print("[ERROR] Missing command line argument! See readme for format.")
            quit()

        #declare gen use variables
        self.wFactor = 1
        self.hFactor = 1
        self.workStr = ""
        
        #NO FONT SCALE:
        #self.regexPression = "\s*((<x>)|(<y>)|(<width>)|(<height>))\d*((<\/x>)|(<\/y>)|(<\/width>)|(<\/height>))"
        
        #FONT SCALE:
        self.regexPression = "\s*((<x>)|(<y>)|(<width>)|(<height>)|(<pointsize>))\d*((<\/x>)|(<\/y>)|(<\/width>)|(<\/height>)|(</pointsize>))"

    #this function isolates the width and height of the resolution input argument
    def getResolution(self, getSplit):
        #find 'x' to create substrings 
        i = 0
        for x in getSplit:
            i += 1
            if x == 'x':
                break
        
        #no 'x', invalid resolution format 
        if i == 0:
            print("[ERROR] Invalid resolution format! See readme for format")
            quit()
        
        #return a touple from input args(width,length)
        resoList = (int(getSplit[:i-1]),int(getSplit[i:]))
        return resoList

    #this function calculates the scale factors for resizing
    def getFactors(self):
        #get inRes, outRes as touple
        splitInRes = self.getResolution(self.inRes)
        splitOutRes = self.getResolution(self.outRes)

        #divide both width and height to find scale factor
        self.hFactor = splitOutRes[1] / splitInRes[1]
        
        self.wFactor = splitOutRes[0] / splitInRes[0]
        #print(str(self.wFactor) + '<-- W factor | H factor -->' + str(self.hFactor))

    def readWrite(self):
        #opens two files, readFile and writeFile
        readFile = open(self.inPath, 'r')
        writeFile = open(self.outPath, 'w')

        #get lines from readFile. Returns a list with all lines within the file
        readLines = readFile.readlines()
        """
        iterate through lines
            Check every line against regex expression to determine if line of interest
                If not line of interest
                    write line as-is
                else
                    line into scale()
                    write line from scale            
        """
        for line in readLines:
            match = re.search(self.regexPression, line)
            if match == None:
                writeFile.write(line)
            else:
                newValue = int(self.scale(line))
                line = re.sub('[0-9]+',str(newValue),line)
                writeFile.write(line)
                
    def scale(self,line):
        #get substring <x>123</x> 123. find first '>', second '<'
        count = 0
        #index of >, second < respectively
        first = 0
        second = 0

        #iterate over line to find char of interest
        for char in line:
            if char == '>':
                first = count
            if char == '<' and first != 0:
                second = count
                break
            count += 1

        #get digit substring
        substr = line[first+1:second]
       
        #if width | x, scale with wFactor
        #  else (height | y), scale with hFactor
        
        if ((str(line[first-1:first]) == "h") or (str(line[first-1:first]) == "x")):
            
            return int(substr) * self.wFactor
            
        else:
            return int(substr) * self.hFactor
       
            

    def primary(self):
        self.getFactors()
        self.readWrite()

        



            
        
