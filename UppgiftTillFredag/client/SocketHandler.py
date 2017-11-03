import socket
import _thread

class SocketHandler:
    # Creates clientsocket
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def setGuiHandler(self,guiHandler_):
        self.guiHandler = guiHandler_

    def connect(self,ip, port):
        # Connects to server and starts recieverthread
        try:
            self.clientSocket.connect((ip,int(port)))
            self.startReceiverThread()
        except:
            return "no connection"

    def sendMsg(self,text):
        # Send msg to server
        try:
            self.clientSocket.send(str.encode(text))
        except:
            pass

    def startReceiverThread(self):
        # Start thread for recv
        _thread.start_new_thread(self.startReceiving,())

    def startReceiving(self):
        while True:
            try:
                # Starts recieveing and prints message in textfield
                msg = self.clientSocket.recv(1024).decode()
                self.guiHandler.showMessage(msg)
            except:
                self.guiHandler.showMessage("desconnected...")
                return