from Data.dataAccess import DataAccess
from Robots.sunflower import Sunflower
from Robots.careobot import CareOBot
from Robots.robotFactory import Factory

import datetime
import cherrypy
import json

class Data(object):
    exposed = True
    
    def __init__(self):
        self._dao = DataAccess()
        
    def GET(self, *args, **kwargs):
        if len(args) < 1:
            raise cherrypy.HTTPError(400)
        
        questionNo = args[0]
        if questionNo == 'current':
            ques = self._dao.getActiveQuestion()
            if ques != None:
                questionNo = ques['sequenceName']
            else:
                questionNo = None
        
        if questionNo != None:
            resp = self._dao.getResponses(questionNo)
            obj = {'query': questionNo, 'responses':resp}
        else:
            obj = {'query': 'none'}
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps(obj)

    def POST(self, *args, **kwargs):
        request = json.loads(cherrypy.request.body.read())
        if not request.has_key('response'):
            raise cherrypy.HTTPError(400)
        else:
            userresponse = int(request['response'])
            if self._dao.setResponse(args[0], userresponse):
                return 'OK'
            else:
                raise cherrypy.HTTPError(500)
            
class UserData(object):
    
    def __init__(self):
        self._dao = DataAccess()
        
    exposed = True

    def GET(self, *args, **kwargs):
        
        if len(args) < 1:
            raise cherrypy.HTTPError(400)
        
        questionNo = args[0]
        if questionNo == 'preferences':
            value = self._dao.getUserPreferences()
        elif questionNo == 'persona':
            value = self._dao.getPersonaValues()
        elif questionNo == 'username': 
            value = self._dao.getActiveUserName()
        
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps(value)
    
    def POST(self, *args, **kwargs):
        
        request = json.loads(cherrypy.request.body.read())

        if request.has_key('time'):
            time = datetime.datetime.now().strftime('%H:%M:%S') #strftime('%Y-%m-%d %H:%M:%S') 
            self._dao.setSessionControlTime(time)
        elif request.has_key('preferences'):
            for column, value in request.iteritems():
                if column != 'preferences':
                    print column + " " + value
                    self._dao.setUserPreferences(column, value)
        else:
            raise cherrypy.HTTPError(400)
            
class RobotCommands(object):
    
    def __init__(self):
        #self._so = Sunflower()
        #self._cob =  CareOBot()
        self._dao = DataAccess()
    
    exposed = True

    def POST(self, *args, **kwargs):
        
        request = json.loads(cherrypy.request.body.read())
        
        # Send the robot to certain location
        if request.has_key('location'):
            object = self._dao.getLocationByName(request['location']);
            robot = Factory.getCurrentRobot();

            robot.setComponentState('tray', request['tray'])
            robot.setComponentState('base', [object['xCoord'], object['yCoord'], object['orientation']])

        # Send voice command to the robot (espeak software required)        
        elif request.has_key('speech'):
            import subprocess
            subprocess.call(['C:\\Program Files (x86)\\eSpeak\\command_line\\espeak.exe', request['speech']])
        else:      
            raise cherrypy.HTTPError(400)      
            
            


