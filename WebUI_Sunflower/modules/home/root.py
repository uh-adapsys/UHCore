import handlers, os#

name = "Home WebPage"
__dir = os.path.dirname(os.path.realpath(__file__))

root = handlers.Index(os.path.join(__dir, 'home.html'))
root.common = handlers.StaticFiles(os.path.join(__dir, '../../common'))
root.images = handlers.StaticFiles(os.path.join(__dir, 'images'))
root.css = handlers.StaticFiles(os.path.join(__dir, 'css'))

from modules.userServices import root as userServices
root.services = userServices

from modules.commands import root as commandsUser
root.commands = commandsUser

from modules.preferences import root as preferencesUser
root.preferences = preferencesUser