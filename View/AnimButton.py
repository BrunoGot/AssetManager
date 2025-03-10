#todo : generate conformed thumbnail automatically if it's not already exist in a thumbnail folder

from PySide2 import QtGui, QtCore, QtWidgets
import os

class AnimButton(QtWidgets.QPushButton):
    '''this class implement the animation button. When its clicked, the animation is playing'''

    def __init__(self,parent=None):
        QtWidgets.QPushButton.__init__(self,parent)

        self.__frames = None
        self.__basePath = None
        self.__framesPath = None
        self.__frameSize = None
        self.__numberOfFrames = None
        self.__timer = RepeatTimer(10,100)
        #self.__timer.setInterval(100)

        self.__isStarted = False #check if the timer is running or not
        self.clicked.connect(self.playAnim)
        self.__timer.timeoutCount.connect(self._setFrame)
        #convertedFrames = self.setFrames(path, frames)

        #self.setIconSize(QtCore.QSize(100,100))
        #self.__timer.start()

    def playAnim(self,index):
        #print("cliiiick")
        if(self.__isStarted==False):
            self.__timer.start()
            self.__isStarted=True
        else:
            self.__timer.stop()
            self.__isStarted = False

    def setFrames(self, basePath=None, frames = [], resizeButton = True, speed = 60):
        # sort the list correctly :
        frames = sorted(frames, key=len)
        selected_frames = []
        """
        #used to optimizez the loading time by reading only one frame of two
        i=0
        for f in frames:
            if i%2==0:
                selected_frames.append(f)
            i+=1"""
        first_few_frames = frames[:50] #just pick up the 10 first frames to avoid blocking process
        selected_frames = first_few_frames
        self.__frames = self._convertFrame(basePath, selected_frames, resizeButton, speed)
        #print("self.__frames = "+str(self.__frames))
        self._setFrame(0)

    def _convertFrame(self, basepath, frames = [], resizeButton = True, speed = 50):
        """load the frames in memory and make it ready to be red by the application"""
        processed = []
        # print(f"convert {frames}")
        for i, f in enumerate(frames):
            pix = QtGui.QPixmap(basepath +"/"+f )
            # print(basepath +"/"+f)


            # todo :crop the f*cking image pix = pix.scaled(1000,100)

            #if it's the first frame, extract the size
            if(i==0):
                self.__frameSize = pix.size()
            #convert to QIcon
            im = QtGui.QIcon(pix)
            processed.append(im)

        self.__numberOfFrames = len(processed)
        self.__basePath = basepath
        self.__framesPath = frames

        self.__timer.numberOfRepeats = self.__numberOfFrames
        self.__timer.delay = speed

        """if resizeButton ==1:
            self.setGeometry(0,0, self.__frameSize.width(), self.__frameSize.height())"""

        return processed

    def _setFrame(self,index=0):
        """this method set wich frame is displayed on the button"""
        if((self.__frames and self.__frameSize and index <=(self.__numberOfFrames-1))==True):
            self.setIcon(self.__frames[index])
            # print("set icon : "+str(self.__frames[index]))
            #self.setIconSize(self.__frameSize)

    def setSize(self, width, height):
        self.setIconSize(QtCore.QSize(width,height))
        #self.setSize()
        self.setGeometry(0, 0, width, height)


class RepeatTimer(QtCore.QTimer):
    #public signal emit when the timeout signal is emitted aswell but passing the iteration index
    timeoutCount = QtCore.Signal(int)
    #public signal wich get fired at the end of all iterations
    endRepeat = QtCore.Signal()

    def __init__(self, numberOfRepeats = 1, delay =10):
        QtCore.QTimer.__init__(self)

        self.__numberOfRepeats =1
        self.numberOfRepeats= numberOfRepeats
        self.__delay = 10
        self.delay = delay
        self.__internalCounter = 0
        self.timeout.connect(self.__eval)

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, value):
        if(value >=0 and type(value).__name__ == "int"):
            self.__delay = value
            self.setInterval(value)

    @property
    def numberOfRepeats(self):
        return self.__numberOfRepeats

    @numberOfRepeats.setter
    def numberOfRepeats(self, value):
        if(value >=0 and type(value).__name__ == "int"):
            self.__numberOfRepeats = value

    def __eval(self):
        if self.__internalCounter >= self.__numberOfRepeats-1:
            self.stop()
            self.endRepeat.emit()
            self.timeoutCount.emit(self.__internalCounter)
            self.__internalCounter = 0

        else:
            self.timeoutCount.emit(self.__internalCounter)
            self.__internalCounter +=1

def main():
    app = QtWidgets.QApplication([])

    path = r"C:\\Users\\Natspir\\NatspirProd\\03_WORK_PIPE\\01_ASSET_3D\\Enviro\\Fog\\FX\\FX\\work_v001\\Flip"
    frames = os.listdir(path)

    temp = AnimButton(path, frames)
    temp.setSize(200,100)
    temp.show()
    app.exec_()

if __name__=="__main__":
    main()
