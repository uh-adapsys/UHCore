import handlers, os#

name = "Preferences WebPage"
__dir = os.path.dirname(os.path.realpath(__file__))

root = handlers.Index(os.path.join(__dir, 'preferences.html'))
root.common = handlers.StaticFiles(os.path.join(__dir, '../../common'))
root.images = handlers.StaticFiles(os.path.join(__dir, 'images'))
root.css = handlers.StaticFiles(os.path.join(__dir, 'css'))