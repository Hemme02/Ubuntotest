import socket
import _thread
import sys
from server.Users import CollectionOfUsers

class SocketHandler:
    # Handles the serversocket
    def __init__(self):
        self.serverSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # Gets the list of users from CollectionOfUsers
        self.users = CollectionOfUsers()
        # Opens the saves userfile and appends it to self.users list
        self.users.readUsersFromFile()

    def setGuiHandler(self,guiHandler_):
        self.guiHandler = guiHandler_

    def closeEveryThing(self):
        # Closes the serversocket and saves the self.users list to the savefile
        self.serverSocket.close()
        self.users.writeUsersToFile()
        sys.exit(0)

    def startAccepting(self):
        while True:
            try:
                # Accepts connection and adds clientsocket and addr to list of unknown clients
                clientSocket, clientAddr = self.serverSocket.accept()
                self.list_of_unknown_clientSockets.append(clientSocket)
                self.list_of_unknown_clientAddr.append(clientAddr)
                # Starts new thread thats recv from clientsocket
                self.startReceiverThread(clientSocket, clientAddr)

            except:
                pass

    def startToAcceptConnection(self,port):
        # Binds the serversocket to port and starts listen
        try:
            self.serverSocket.bind(('',int(port)))
        except:
            return "failed"
        self.serverSocket.listen()

        self.list_of_known_clientSockets = []
        self.list_of_known_clientAddr = []

        self.list_of_unknown_clientSockets = []
        self.list_of_unknown_clientAddr = []
        # Starts new thread thats waiting for accepted connection
        _thread.start_new_thread(self.startAccepting,())
        return "succeed"

    def sendAndShowMsg(self, text):
        # Prints message in textfield and broadcasts it to all clients in list_of_known clients
        self.guiHandler.showMessage(text)
        for clientSock in self.list_of_known_clientSockets:
            clientSock.send(str.encode(text))

    def startReceiverThread(self, clientSocket, clientAddr):
        # Thread thats recv
        _thread.start_new_thread(self.startReceiving,(clientSocket,clientAddr,))

    def startReceiving(self,clientSocket, clientAddr):
        # Function that lets the client log in and in case of succesful login the user gets appenden to list_of_known_client
        resultOfLogin = self.listenToUnknownClinet(clientSocket,clientAddr)

        if resultOfLogin !=False:
            username = resultOfLogin
            self.list_of_unknown_clientSockets.remove(clientSocket)
            self.list_of_unknown_clientAddr.remove(clientAddr)

            self.list_of_known_clientSockets.append(clientSocket)
            self.list_of_known_clientAddr.append(clientAddr)
            # Starts function that listens to clientsocket and broadcasts msg from client
            self.listenToknownClinet(clientSocket,clientAddr,username)

    def listenToUnknownClinet(self,clientSocket, clientAddr):
        # Function that lets the client login
        while True:
            try:
                msg = clientSocket.recv(1024).decode()
            except:
                # Handles error if client disconnects
                self.list_of_unknown_clientSockets.remove(clientSocket)
                self.list_of_unknown_clientAddr.remove(clientAddr)
                return False

            # Checks if msg is three diffrent words, login, username and password
            args = msg.split(' ')
            if len(args) == 3 and args[0] == "login":
                username = args[1]
                password = args[2]
                # Checks if username and password matches and that the client isnt already logged in
                if self.users.doesThisUserExistAndNotActive(username,password):
                    clientSocket.send(str.encode("ok"))
                    self.sendAndShowMsg(username + " is connected")
                    return username
                else:
                    clientSocket.send(str.encode("not ok"))

            # Checks if msg is more than five words and in that case if first word is register
            if len(args) >= 5 and args[0] == "register":
                username = args[1]
                password = args[2]
                email = args[3]
                name = ""
                # Since name can be more than one word a for loop is used
                for rest in args[4:]:
                    name += rest + " "
                # Checks that no value is empty
                if username != "" and password != "" and email != "" and name != "":
                    # Adds new user
                    resultOfAdding = self.users.add_user(username,password,email,name)
                    if resultOfAdding == True:
                        clientSocket.send(str.encode("fine"))
                    else:
                        clientSocket.send(str.encode("not fine"))
                else:
                    clientSocket.send(str.encode("not fine"))

    def listenToknownClinet(self,clientSocket, clientAddr,username):
        while True:
            try:
                # Revieces msg from clients and broadcasts it to all connected clients
                msg = clientSocket.recv(1024).decode()
                self.sendAndShowMsg(username + ": " + msg)
            except:
                # Except to pick up error when client disconnects and removes socket and addr from their lists
                self.list_of_known_clientSockets.remove(clientSocket)
                self.list_of_known_clientAddr.remove(clientAddr)
                self.sendAndShowMsg(username+" disconnected")
                self.users.inactiveUser(username)
                return
