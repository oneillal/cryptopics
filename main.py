from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import os
import struct
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA512
#from Crypto.Protocol.KDF import PBKDF2
from pbkdf2 import PBKDF2
from PIL import Image




def print_no_pwd_msg():
   	tkMessageBox.showinfo("Password required", "Please enter a password before selecting a file.")

def open_image():
	# check whether a password has been entered
	if ( app.passwd.get() ):
		print app.passwd.get()
		filename = askopenfilename()
        	directory = os.path.dirname(filename)
		encrypt(filename, app.passwd.get())
	# if no pwd, then show pop-up message
	else:
		print_no_pwd_msg()

def encrypt(filename, password):
	outfilename = filename + ".crypt"


	key_size = 32
	iterations = 40000
	hash = SHA512
	bs = AES.block_size
	salt_marker = b'$'
	header = salt_marker + struct.pack('>H', iterations) + salt_marker
	#salt = os.urandom(32).encode('hex')
	salt = Random.new().read( key_size )

	kdf = PBKDF2(password, salt, iterations, hash)
	print kdf
	
	key = kdf.read(key_size)
	print key

	print AES.block_size
	iv = Random.new().read( bs )
	cipher = AES.new(key, AES.MODE_CBC, iv)
	
	outfilename = open(outfilename, 'wb')
	outfilename.write( header + salt )
	outfilename.write( iv )

	filename = open(filename, 'rb')

	finished = False

	while not finished:
        	chunk = filename.read(1024 * bs)

        	if len(chunk) == 0 or len(chunk) % bs != 0:
            		padding_length = (bs - len(chunk) % bs) or bs
            		chunk += (padding_length * chr(padding_length)).encode()
            		finished = True

		outfilename.write(cipher.encrypt(chunk))

def decrypt(filename, password):
	outfilename = filename + ".crypt"
        key_size = 32
        iterations = 40000
        hash = SHA512
        bs = AES.block_size
        salt_marker = b'$'
        header = salt_marker + struct.pack('>H', iterations) + salt_marker
        #salt = os.urandom(32).encode('hex')
        salt = Random.new().read( key_size )

        kdf = PBKDF2(password, salt, iterations, hash)
        print kdf
        
        key = kdf.read(key_size)
        print key

        print AES.block_size
        iv = Random.new().read( bs )
        cipher = AES.new(key, AES.MODE_CBC, iv)




class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


    def createWidgets(self):

	# password input
	self.passwdLabel = Label(self, text="Enter password to encrypt/decrypt image:")
	self.passwdLabel.pack()
	self.passwd = Entry(self, show="*", width=30)
	self.passwd.pack()

	# quit button
        self.quit = Button(self, text="Quit", command=self.quit)
        self.quit.pack({"side": "bottom"})

	# select image button
        self.selectImg= Button(self, text="Select Image")
        self.selectImg["command"] = open_image
        self.selectImg.pack({"side": "left"})



# initialize the GUI
root = Tk()

# set the title of the window
root.title("Image Crypt")

# set the size of the window
window = Canvas(root, width=400, height=100)
window.pack()

# instantiate the application
app = Application(master=root)
app.mainloop()
