
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
		print 'PASSWORD: ' + app.passwd.get()
		filename = askopenfilename()
        	directory = os.path.dirname(filename)
		infile, file_extension = os.path.splitext(filename)
		
		if( file_extension == ".cryptopics" ):
			decrypt( filename, app.passwd.get() )
		else:
			encrypt(filename, app.passwd.get())
	
	# if no pwd, then show pop-up message
	else:
		print_no_pwd_msg()


def encrypt(filename, password):
	outfile = filename + ".cryptopics"

	key_size = 32
	iterations = 40000
	hash = SHA512
	bs = AES.block_size
	print "BLOCK SIZE: " , bs
	salt_marker = b'$'
	header = salt_marker + struct.pack('>H', iterations) + salt_marker

	salt = Random.new().read( key_size )
	
	kdf = PBKDF2(password, salt, iterations, hash)
	print "KDF: " , kdf
	
	key = kdf.read(key_size)
	print 'KEY: ' , key

	iv = Random.new().read( bs )
	cipher = AES.new(key, AES.MODE_CBC, iv)
	print 'CIPHER: ' , cipher
	
	outfile = open(outfile, 'wb')
	print 'HEADER: ', header
	print 'SALT: ', salt
	outfile.write( header + salt )
	outfile.write( iv )
	print 'IV: ' , iv

	infile = open(filename, 'rb')

	finished = False

	while not finished:
        	chunk = infile.read(1024 * bs)

        	if len(chunk) == 0 or len(chunk) % bs != 0:
            		padding_length = (bs - len(chunk) % bs) or bs
            		chunk += (padding_length * chr(padding_length)).encode()
            		finished = True

		outfile.write(cipher.encrypt(chunk))

def decrypt(filename, password):
	outfile, file_extension = os.path.splitext(filename)
	outfile, file_extension = os.path.splitext(outfile)
	print "OUTFILE: " + outfile
	#outfilename = filename + ".crypt"
	outfile = outfile + "_decrypted.png"
	outfile = open(outfile, 'wb')

        key_size = 32
        iterations = 40000
        hash = SHA512
        bs = AES.block_size
	print 'bs: ', bs
        salt_marker = b'$'
        #header = salt_marker + struct.pack('>H', iterations) + salt_marker

	filename = open(filename, 'rb')
        salt = filename.read( bs )

        kdf = PBKDF2(password, salt, iterations, hash)
        print kdf
        
        key = kdf.read(key_size)
        print key

        iv = filename.read( bs )
        cipher = AES.new(key, AES.MODE_CBC, iv)
	
	next_chunk = b''
	finished = False

	while not finished:
        	chunk, next_chunk = next_chunk, cipher.decrypt(infile.read(1024 * bs))
        	print ("CHUNK: " , chunk)
        	print ("NEXT_CHUNK: " , next_chunk)

        	if not next_chunk:
        		padlen = chunk[-1]
                if isinstance(padlen, str):
                	padlen = ord(padlen)
                	padding = padlen * chr(padlen)
                else:
                	padding = (padlen * chr(chunk[-1])).encode()

                if padlen < 1 or padlen > bs:
                	raise ValueError("bad decrypt pad (%d)" % padlen)

                # all the pad-bytes must be the same
                if chunk[-padlen:] != padding:
                	# this is similar to the bad decrypt:evp_enc.c
                	# from openssl program
                	raise ValueError("bad decrypt")

                chunk = chunk[:-padlen]
                finished = True

        	outfile.write(chunk)

	




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
        self.selectImg = Button(self, text="Select Image")
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
