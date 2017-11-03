from GuiHandler import GuiHandler
from SocketHandler import SocketHandler

# Creates clientobject
socketHandler = SocketHandler()
# Connects gui to clientobject
guiHandler = GuiHandler(socketHandler)
socketHandler.setGuiHandler(guiHandler)

# Gets ip and port from GUI
ip,port = guiHandler.getIpAndPort()

# Starts connection to server
resultOfConnection = socketHandler.connect(ip,port)
if resultOfConnection == "no connection":
    guiHandler.showWarningMsg()
else:
    guiHandler.startGui()
