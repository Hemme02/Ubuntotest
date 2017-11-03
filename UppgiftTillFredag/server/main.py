from server.GuiHandler import GuiHandler
from server.SocketHandler import SocketHandler

# Creates serverobject
socketHandler = SocketHandler()
# Connects gui to serverobject
guiHandler = GuiHandler(socketHandler)
socketHandler.setGuiHandler(guiHandler)

# Get port to serverobject
port = guiHandler.getPort()
# Starts gui if socket can be bound to port
resultOfBinding = socketHandler.startToAcceptConnection(port)

if resultOfBinding == "failed":
    guiHandler.showWarningMsg()
else:
    guiHandler.startGui()

