import tkinter
import tkinter.messagebox

class GuiHandler:
    # Handles the GUI
    def __init__(self,socketHandler_):
        self.socketHandler = socketHandler_

    def getPort(self):
        # GUI to get Port to server
        rootToGetPort = tkinter.Tk()
        lab = tkinter.Label(rootToGetPort,text="port")
        lab.grid(row = 0, column = 0)
        entOfPort = tkinter.Entry(rootToGetPort)
        entOfPort.grid(row = 0, column = 1)

        self.portToReturn = ""
        def confirmPort():
            # Sub func to get entered port. No control for empty entry
            self.portToReturn = entOfPort.get()
            rootToGetPort.destroy()
        but = tkinter.Button(rootToGetPort,text="set port",bg='blue', fg='white', command = confirmPort)
        but.grid(row = 1, column = 0)
        rootToGetPort.mainloop()
        return self.portToReturn

    def startMainGui(self):
        # Main GUI
        self.root = tkinter.Tk()

        # Code for scrollbar
        scroll = tkinter.Scrollbar(self.root)

        # Sticky can also be 'ns'
        scroll.grid(row = 0, column = 1, sticky=tkinter.N+tkinter.S)


        self.chattContents = tkinter.Text(self.root, yscrollcommand  = scroll.set)
        self.chattContents.grid(row = 0,column = 0)
        scroll.config(command=self.chattContents.yview)
        self.entryOfUser = tkinter.Entry(self.root)
        self.entryOfUser.grid(row = 1,column = 0)

        # Creates send and quit button
        self.buttonToTrigg = tkinter.Button(self.root, text = "enter", command = self.sendMsgBySocketHandler)
        self.buttonToTrigg.grid(row = 1,column = 1)
        self.buttonToTrigg = tkinter.Button(self.root, text = "close", command = self.closeConnection)
        self.buttonToTrigg.grid(row = 2,column = 0)
        self.root.mainloop()

    def sendMsgBySocketHandler(self):
        # Send inputed message
        self.socketHandler.sendAndShowMsg("Admin: " + self.entryOfUser.get())

    def closeConnection(self):
        # Closes all open sockets
        self.socketHandler.closeEveryThing()

    def startGui(self):
        # Starts mainGui
        self.startMainGui()

    def showMessage(self,text):
        # Inserts message to textwindow
        self.chattContents.insert(tkinter.END,text+"\n")

    def showWarningMsg(self):
        # Alert if error happens when binding port
        tkinter.messagebox.showwarning(message="could not bind port")