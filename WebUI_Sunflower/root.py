import handlers, os
from common.scripts.httpRequests import Data, UserData, RobotCommands

name = "Site Root"

root = handlers.Index(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dirIndex.html'))
root.js = handlers.StaticFiles(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'common/js'))
root.css = handlers.StaticFiles(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'common/css'))
root.images = handlers.StaticFiles(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'common/images'))
root.favicon_ico = handlers.StaticFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'favicon.ico'))
root.data = Data()
root.userdata = UserData()
root.command = RobotCommands()

from modules.home import root as homeRoot
root.home = homeRoot