class Model:

        def __init__(self):

            self.pointFilePath = None
            self.pointFileContent = None
            self.pointList = None
            self.setFilePath = None
            self.setFileContent = None
            self.setList = None
            self.xmlFilePath = None
            self.xmlFileContent = None

        def isValid( self, fileName ):

            try: 
                file = open( fileName, 'r' )
                file.close()
                return True
            except:
                return False

        def setPointFilePath( self, fileName ):

            if self.isValid( fileName ):
                self.pointFilePath = fileName
                self.pointFileContent = open( fileName, 'r' ).readlines()
                self.pointList = self.getPoints()
            else:
                self.pointFilePath = None
                self.pointFileContent = ''

        def setSetFilePath( self, fileName ):

            if self.isValid( fileName ):
                self.setFilePath = fileName
                self.setFileContent = open( fileName, 'r' ).readlines()
                self.setList = self.getSets()
            else:
                self.setFilePath = None
                self.setFileContent = ''

        def setXMLFilePath( self, fileName ):

            self.xmlFilePath = fileName

        def getXMLFilePath( self ):

            return self.xmlFilePath

        def getSetFilePath( self ):

            return self.setFilePath

        def getPointFilePath( self ):

            return self.pointFilePath

        def getXMLFileContents( self ):

            return self.pointFileContent

        def getSetFileContents( self ):

            return self.setFileContent

        def getPointFileContents( self ):
     
            return self.xmlfileContent

        def getPoints(self):

            pointList = []

            for point in self.pointFileContent:

                pt = point.split(',')
                tempPoint = Point(pt[0],pt[1],pt[2],pt[3],pt[4].strip('\n'))
                pointList.append(tempPoint)

            return pointList

        def getSets(self):

            setline = False

            setList = []

            tempSet = Set(0,'', [])

            for line in self.setFileContent:

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