
from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import os
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA512
from pbkdf2 import PBKDF2


KEY_SIZE = 32
ITERATIONS = 40000
HASH = SHA512
BLOCK_SIZE = AES.block_size


def print_no_pwd_msg():
   	tkMessageBox.showinfo("Password required", "Please enter a password before selecting a file.")


def open_image():
	# check whether a password has been entered
	if ( app.passwd.get() ):
		
		# open window to choose the desired file
		filename = askopenfilename()
		
		# extract the file name and its extension
		infile, file_extension = os.path.splitext(filename)
		
		# it will decrypt the file if its extension is .cryptopics
		if( file_extension == ".cryptopics" ):
			decrypt( filename, app.passwd.get() )
		# otherwise it will encrypt
		else:
			encrypt( filename, app.passwd.get() )
	
	# if no pwd, then show pop-up message
	else:
		print_no_pwd_msg()


def encrypt(filename, password):

	# append ".cryptopics" to the encrypted file name that will be created
	outfile = filename + ".cryptopics"

	# create a 32 byte long random salt
	salt = Random.new().read( KEY_SIZE )
	
	"""
		kdf = key derivation function
		- this function will derive a key from the password
		- additional security so that when decrypting the image it's necessary
		  to know the size of the salt hash, the number of iterations, the
		  hash used, the block size and the password itself
	
		- References
		https://www.dlitz.net/software/pycrypto/api/2.6/Crypto.Protocol.KDF-module.html
		https://en.wikipedia.org/wiki/Rainbow_table
	"""
	kdf = PBKDF2(password, salt, ITERATIONS, HASH)
	
	# the key created by the kdf will be used to encrypt the data
	key = kdf.read( KEY_SIZE )

	"""
		- create a cypher that we will use to encrypt the data
		- this cypher is created with a key, a block cipher mode and an IV(initialization vector)
		- The IV is a data block that is used for encryption and decryption

		- References
		https://www.dlitz.net/software/pycrypto/api/2.6/Crypto.Cipher.AES-module.html
		https://www.dlitz.net/software/pycrypto/api/2.6/Crypto.Cipher.blockalgo-module.html#MODE_CBC
	"""
	iv = Random.new().read( BLOCK_SIZE )
	cipher = AES.new(key, AES.MODE_CBC, iv)
	
	# open a new file for writing in binary mode
	outfile = open(outfile, 'wb')

	# write the salt and the IV
	outfile.write( salt + iv )

	# open file-to-be-encrypted for reading in binary mode
	infile = open(filename, 'rb')

	# this loop will go through the file(picture) until the end.
	# it will also pad encoded zero's if a chunk of data is not multiple of 16
	while True:
		# reads data in chunks of 16KB
		data = infile.read( 1024 * BLOCK_SIZE )
		
		# check whether the length of data is not multiple of 16
		if  len(data) % BLOCK_SIZE != 0:
			# find the number of bytes that will need to be filled with zero's
			data_padding = BLOCK_SIZE - len(data) % BLOCK_SIZE
			
			# append the encoded zero's ('\x00') to the data to complete a block of 16 bytes
			data += (data_padding * chr(0)).encode()

		# get out of loop when there is no more data to write in to the file
		if data == '':
			break

		"""
			- AES(Advanced Encryption Standard) has a fixed data block size of 16 bytes
			- The data passed in to the encrypt() function must be multiple of 16
			
			- References
			https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
		"""
		
		outfile.write(cipher.encrypt(data))


def decrypt(filename, password):

	# extract the file name and its extension
	outfile, file_extension = os.path.splitext(filename)

	# since we only decrypt ".cryptopics" extension, it needs to extract the file extension twice
	outfile, file_extension = os.path.splitext(outfile)

	# appends "_decrypted" to the name of the original file
	outfile = outfile + "_decrypted" + file_extension

	# open the encrypted file for reading in binary mode
	infile = open(filename, 'rb')

	# reads the salt from the encrypted file
        salt = infile.read( KEY_SIZE )

	# derive the key from the password
        kdf = PBKDF2(password, salt, ITERATIONS, HASH)
        
        key = kdf.read( KEY_SIZE )

	# reads the IV that was put in the file when encrypting it
        iv = infile.read( BLOCK_SIZE )

	# creates the AES symmetric cipher to decrypt the data
        cipher = AES.new(key, AES.MODE_CBC, iv)
	
	# "b''" represents a binary file which is necessary to initialize the file
	data = b''

	# open a new file to write the decrypted data for writing in binary mode
	outfile = open(outfile, 'wb')

	# loop to go through the encrypted data in the file
	while data is not None:

		# write encrypted data in to the new file
		outfile.write(data)

		# grab chunks of 16KB of decrypted data
		data = cipher.decrypt(infile.read(1024 * BLOCK_SIZE))
		
		# exit the loop when there is no more data to read from the encrypted file
		if data == '':
			data = None

# a class to set up a create the GUI
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
        self.selectImg.pack()



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
