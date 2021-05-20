import shutil
import os

class Set(object):

    def __init__(self, setId, descriptor,points):

        self.setId = setId
        self.descriptor = descriptor
        self.points = points

    def __str__(self):

        return self.setId + ' ' + self.descriptor + '\n' + str(self.points)

class Point(object):

    def __init__(self,pId,north,east,height,descriptor):

        self.pId = pId
        self.north = north
        self.east = east
        self.height = height
        self.descriptor = descriptor

class LandXML(object):

    def __init__(self,pointList,setList,filename):


        self.setList = setList
        self.pointList = pointList
        self.filename = filename

    def outputLandXML(self):

        src = os.getcwd() + '/landxmlutmheader.txt'
        dst = os.getcwd() + '/' + self.filename
        shutil.copyfile(src, dst)

        landXML = open(dst, 'a')
        print('bamn')

        landXML.write('\t<CgPoints>\n')

        for point in self.pointList:
            lineString = '\t\t<CgPoint name=\"' 
            lineString = lineString + point.pId
            lineString = lineString + ' \" '
            lineString = lineString + 'code=\"'
            lineString = lineString + point.descriptor
            lineString = lineString + '\">'
            lineString = lineString + str(point.north) + ' '
            lineString = lineString + str(point.east) + ' '
            lineString = lineString + str(point.height) + '</CgPoint>\n'

            landXML.write(lineString)

        landXML.write('\t</CgPoints>\n') 

        for pSet in self.setList:

            lineString = '\t<CgPoints name=\"' + pSet.descriptor + '\">\n'
            landXML.write(lineString)

            for point in pSet.points:

                pointString = '\t\t<CgPoint pntRef=\"' + str(point) + '\"/>\n'
                landXML.write(pointString)

            endTagString = '\t</CgPoints>\n'
            landXML.write(endTagString)

        landXML.write('</LandXML>')        

def getPoints(pointfile):

    pointList = []

    for point in pointfile.readlines():

        pt = point.split(',')
        tempPoint = Point(pt[0],pt[1],pt[2],pt[3],pt[4].strip('\n'))
        pointList.append(tempPoint)

    return pointList

def getSets(setfile):

    setline = False

    setList = []

    tempSet = Set(0,'', [])

    for line in setfile.readlines():

        if setline == True and not 'COORDINATE' in line.split(' ') and not 'Page' in line.split(' '):
            pointRanges = line.split(', ')

            for pRange in pointRanges:
                points = pRange.split('-')
                
                if len(points) > 1:

                    indexi = int(points[0])
                    indexf = int(points[1])

                    if indexi > indexf:

                        for i in range(indexf,indexi+1):
                            
                            tempSet.points.append(i)

                    else:

                        for i in range(indexi,indexf+1):

                            tempSet.points.append(i)
                
                else:

                    tempSet.points.append(int(i))
                    
            tempSet.points = set(tempSet.points)
            setline=False
            setList.append(tempSet)
            tempSet = Set(0,'', [])

        elif line[0:3] == 'SET':
            
            x = line.split(' ')
            tempSet.setId = x[1]
            
            descriptorString = ''

            for word in x[2:len(x)-1]:

                descriptorString = descriptorString + word + ' '
            
            tempSet.descriptor = descriptorString + x[len(x)-1].strip('\n')

            setline = True
        
    return setList
            

setfile = open('SET FILE.txt','r')
pointfile = open('TRANS221.TXT','r')

sets = getSets(setfile)
points = getPoints(pointfile)

landxml = LandXML(points, sets,'SetConvert.xml')
landxml.outputLandXML()