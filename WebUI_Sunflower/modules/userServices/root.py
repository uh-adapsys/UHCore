import handlers, os#

name = "User Services"
__dir = os.path.dirname(os.path.realpath(__file__))

root = handlers.Index(os.path.join(__dir, 'userServices.html'))
root.common = handlers.StaticFiles(os.path.join(__dir, '../../common'))
root.images = handlers.StaticFiles(os.path.join(__dir, 'images'))
root.css = handlers.StaticFiles(os.path.join(__dir, 'css'))
root.favicon_ico = handlers.StaticFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../favicon.ico'))