from Tkinter import *
from tkFileDialog import *
import os

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"
	filename = askopenfilename()
        file_path_d = os.path.dirname(filename)
	print '"' + filename + '"'

    def createWidgets(self):

	passlabel = Label(self, text="Enter Key to encrypt/deccrypt image:")
	passlabel.pack()
	passg = Entry(self, show="*", width=20)
	passg.pack()

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "SelectImage",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk(className="Image crypt")
labelframe = LabelFrame(root, text="This is a LabelFrame")
labelframe.pack(fill="both", expand="yes")
app = Application(master=root)
app.mainloop()
#root.destroy()
