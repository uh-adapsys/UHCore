from Data.dataAccess import DataAccess, Locations
from config import server_config
from extensions import PollingProcessor
import math

class LocationProcessor(PollingProcessor):
    
    def __init__(self):
        super(LocationProcessor, self).__init__()
        self._dao = DataAccess()
        self._storedLoc = lambda: {'locationName': '', 'xCoord': 0, 'yCoord': 0, 'orientation': 0, 'driftThreshold': 0 }
        self._curLoc = lambda: ('', (0, 0, 0))
        self._updateLoc = lambda locid, x, y, orientation: True
        self._targetName = ''
    
    def start(self):
        print "Started polling location for %s" % (self._targetName)
        self._addPollingProcessor('location', self.checkUpdateLocation, (self._curLoc, self._storedLoc, self._updateLoc), 2)

    def stop(self):
        print "Stopped polling location for %s" % (self._targetName)
        self._removePollingProcessor('location')
    
    def checkUpdateLocation(self, getCurrentLocation, getSavedLocation, updateLocation):
        savedLoc = getSavedLocation()
        (name, (x, y, orientation)) = getCurrentLocation()

        if x == None or y == None:
            return
        
        update = False
        if name != savedLoc['locationName']:
            update = True
        else:
            dist = 0
            dist += math.pow(x - savedLoc['xCoord'], 2)
            dist += math.pow(y - savedLoc['yCoord'], 2)
            dist = math.sqrt(dist)
            if not savedLoc.has_key('driftThreshold') or dist > savedLoc['driftThreshold']:
                update = True
            else:
                if abs(savedLoc['orientation'] - orientation) > 5:                     
                    update = True

        if update:
            loc = self._dao.getLocationByName(name)
            if loc == None:
                locid = None
            else:
                locid = loc['locationId']
            print "Updating %(target)s location to Name:%(name)s, X:%(x)s, Y:%(y)s, O:%(orientation)s" % dict({'target':self._targetName}.items() + locals().items())
            updateLocation(locid, x, y, orientation)

class RobotLocationProcessor(LocationProcessor):
    
    def __init__(self, robot=None):
        super(RobotLocationProcessor, self).__init__()
        if robot == None:
            from Robots.robotFactory import Factory
            self._robot = Factory.getCurrentRobot()
        else:
            self._robot = robot

        robId = self._dao.getRobotByName(self._robot.name)['robotId']
        self._targetName = self._robot.name
        self._storedLoc = lambda: self._dao.getRobot(robId)
        self._curLoc = lambda: self._robot.getLocation(False)        
        self._updateLoc = lambda locid, x, y, orientation: self._dao.saveRobotLocation(robId, locid, x, y, orientation)

class HumanLocationProcessor(LocationProcessor):
    
    def __init__(self):        
        super(HumanLocationProcessor, self).__init__()
        
        from Robots.rosHelper import ROS, Transform
        self._ros = ROS()
        self._topic = '/trackedHumans'
        self._tm = None        
        self._transform = Transform(toTopic='/map', fromTopic='/room_frame')
        
        self._targetName = "Humans"
        self._storedLoc = self._getStoredLoc
        self._curLoc = self._getCurrentLoc
        self._updateLoc = lambda locid, x, y, orientation: self._update(locid, x, y, orientation)
    
    @property
    def _transformMatrix(self):
        if self._tm == None:
            ((x, y, _), rxy) = self._transform.getTransform()
            if x == None or y == None:
                return ('', (None, None, None))
            
            angle = round(math.degrees(rxy))
            self._tm = (round(x, 3), round(y, 3), angle)
        
        return self._tm

    def _update(self, locid, x, y, theta):
        self._dao.locations.saveLocation(999, 999, x, y, theta, server_config['mysql_location_table'], 'locationId')
    
    def _getCurrentLoc(self):

        locs = self._ros.getSingleMessage(self._topic)
        if len(locs.trackedHumans) > 0:
            loc = locs.trackedHumans[0]
        else:
            return ('', (None, None, None))
        
        x = loc.location.point.x + self._transformMatrix[0]
        y = loc.location.point.y + self._transformMatrix[1]
        angle = 0 + self._transformMatrix[2]
        print "Using human location from id: %s" % loc.id
        
        pos = (round(x, 3), round(y, 3), angle)        
        return Locations.resolveLocation(pos)
    
    def _getStoredLoc(self):
        loc = self._dao.getLocation(999)
        loc['locationName'] = loc['name']
        return loc
    
if __name__ == '__main__':
    import sys
    lp = HumanLocationProcessor()
    lp.start()
    while True:
        try:
            sys.stdin.read()
        except KeyboardInterrupt:
            break
    lp.stop()
