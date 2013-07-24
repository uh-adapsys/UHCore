import sys
import time
import robot
import random

class DummyRobot(robot.Robot):
    _imageFormats = ['BMP', 'EPS', 'GIF', 'IM', 'JPEG', 'PCD', 'PCX', 'PDF', 'PNG', 'PPM', 'TIFF', 'XBM', 'XPM']

    def __init__(self, name):
        super(DummyRobot, self).__init__(name, DummyInterface, '', '')
        self._states = {}
               
    def getCameraAngle(self):
        time.sleep(random.randrange(0, 10, 1) / 10.0)
        return 0

    def getComponentState(self, componentName, dontResolveName=False):
        if self._states.has_key(componentName):
            return (self._states[componentName], self._states[componentName])
        return ('', None)
                
    def setComponentState(self, name, value, blocking=True):
        if blocking:
            time.sleep(random.randrange(1, 20, 1) / 2.0)
            self._states[name] = value
            return 'SUCCESS'
        else:
            self._states[name] = value
            return 'ACTIVE'
    
    def play(self, fileName, blocking=True):
        self.executeFunction("play", {
                                      'parameter_name':fileName,
                                      'blocking':blocking
                                      })
    
    def say(self, text, languageCode="en-gb", blocking=True):
        self.executeFunction("say", {
                                     'parameter_name': [text,],
                                     'blocking': blocking })
        
    def sleep(self, milliseconds):
        self.executeFunction("sleep", {'duration': milliseconds / 1000.0 })
        
class DummyInterface(object):
    
    def __init__(self):
        pass
        
    def runFunction(self, funcName, kwargs):
        blocking = True
        if kwargs.has_key('blocking'):
            blocking = bool(kwargs['blocking'])
        if blocking:
            time.sleep(random.randrange(1, 10, 1) / 2.0)
            return 3
        else:
            return 1
        
    def initComponent(self, name):
        return 3
    
    def runComponent(self, name, value, mode=None, blocking=True):
        if(blocking):
            time.sleep(random.randrange(1, 10, 1) / 2.0)
            return 3
        else:
            return 1

class PoseUpdater(robot.PoseUpdater):
    def __init__(self, robot):
        super(PoseUpdater, self).__init__(robot)
    
    def checkUpdatePose(self, robot):
        states = {}
        states.update(self.getTrayStates(robot))
        states.update(self.getHeadStates(robot))
        self.updateStates(states)

    def getHeadStates(self, robot):
        return {
                   'eyePosition': 'Front',
                   }

    def getTrayStates(self, robot):
        return {
                   'trayStatus': 'raised',
                   'trayIs': 'Empty' }
            
if __name__ == '__main__':
    from robotFactory import Factory
    robot = Factory.getCurrentRobot()
    
    import locations
    from history import SensorLog
    l = locations.RobotLocationProcessor(robot)
    rp = PoseUpdater(robot)
    sr = SensorLog(rp.channels, rp.robot.name)

    rp.start()
    sr.start()
    
    l.start()
    
    while True:
        try:
            sys.stdin.read()
        except KeyboardInterrupt:
            break
    l.stop()

    sr.stop()
    rp.stop()
