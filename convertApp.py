# MyApp.py
# D. Thiebaut
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from mainwindow import Ui_MainWindow
import sys
import os, shutil
from model import Model, Set, Point, LandXML

class MainWindowUIClass( Ui_MainWindow ):
    def __init__( self ):
        '''Initialize the super class
        '''
        super().__init__()
        self.model = Model()

    def setupUi( self, MW ):
        ''' Setup the UI of the super class, and add here code
        that relates to the way we want our UI to operate.
        '''
        super().setupUi( MW )

        # close the lower part of the splitter to hide the 
        # debug window under normal operations

    def debugPrint( self, msg ):
        '''Print the message in the text edit at the bottom of the
        horizontal splitter.
        '''
        print( msg )

    # slot
    def slotSetFilePath( self ):
        ''' Called when the user enters a string in the line edit and
        presses the ENTER key.
        '''
        self.debugPrint( "RETURN key pressed in Set File Path" )

    # slot
    def slotXMLFilePath( self ):
        ''' Called when the user enters a string in the line edit and
        presses the ENTER key.
        '''
        self.debugPrint( "RETURN key pressed in XML File Path" )

    # slot
    def slotPointFilePath( self ):
        ''' Called when the user enters a string in the line edit and
        presses the ENTER key.
        '''
        self.debugPrint( "RETURN key pressed in Point File Path" )

    # slot
    def slotCreateLandXML( self ):
        ''' Called when the user presses the Write-Doc button.
        '''
        self.debugPrint( "Create XML button pressed" )

        src = os.getcwd() + '/landxmlutmheader.txt'
        dst = self.model.xmlFilePath
        shutil.copyfile(src, dst)

        landXML = open(dst, 'a')
        print('bamn')

        landXML.write('\t<CgPoints>\n')

        for point in self.model.pointList:
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

        for pSet in self.model.setList:

            lineString = '\t<CgPoints name=\"' + pSet.descriptor + '\">\n'
            landXML.write(lineString)

            for point in pSet.points:

                pointString = '\t\t<CgPoint pntRef=\"' + str(point) + '\"/>\n'
                landXML.write(pointString)

            endTagString = '\t</CgPoints>\n'
            landXML.write(endTagString)

        landXML.write('</LandXML>')

    # slot
    def slotBrowseSet( self ):
        ''' Called when the user presses the Browse button
        '''
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "All Files (*);;Python Files (*.py)",
                        options=options)
        if fileName:
            self.debugPrint( "setting file name: " + fileName )
            self.model.setSetFilePath( fileName )
            self.lineEdit.setText( self.model.getSetFilePath() )

    def slotBrowseXML( self ):
        ''' Called when the user presses the Browse button
        '''
        self.debugPrint( "XML Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
                        None,
                        "QFileDialog.getSaveFileName()",
                        "",
                        "All Files (*);;Python Files (*.py)",
                        options=options)
        if fileName:
            self.debugPrint( "setting file name: " + fileName )
            self.model.setXMLFilePath( fileName )
            self.lineEdit_5.setText( self.model.getXMLFilePath() )
            self.debugPrint( self.model.getXMLFilePath() )
            self.debugPrint( "bamn" )


    def slotBrowsePoint( self ):
        ''' Called when the user presses the Browse button
        '''
        self.debugPrint( "Point Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "All Files (*);;Python Files (*.py)",
                        options=options)
        if fileName:
            self.debugPrint( "setting file name: " + fileName )
            self.model.setPointFilePath( fileName )
            self.lineEdit_2.setText( self.model.getPointFilePath() )

def main():
    """
    This is the MAIN ENTRY POINT of our application.  The code at the end
    of the mainwindow.py script will not be executed, since this script is now
    our main program.   We have simply copied the code from mainwindow.py here
    since it was automatically generated by '''pyuic5'''.

    """
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUIClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

main()