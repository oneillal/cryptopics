# Crypto Pics

A Python based image encrypter application developed for NCP Hip in Cyber Security 2017.  

![alt text](https://github.com/oneillal/cryptopics/raw/master/doc/crypto-pics.png "UI")

### Prerequisites  
  * Python >2.7  

```
root@kali:~# python --version 
Python 2.7.13
```

### Dependencies  
The below Python module dependencies are needed to build. These are all pre-installed on Kali Linux.
  * pycrypto  
  * tkinter  

### Cloning the Git Repo  

```
root@kali:~# git clone https://github.com/oneillal/cryptopics.git
```

### Running the Program 

``` 
root@kali:~# cd cryptopics
root@kali:~# python ./main.py
```

### Python Code

```python
import time
import ttk
from PIL import ImageTk
from Tkinter import *
from tkFileDialog import *
import PIL.Image
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
   	tkMessageBox.showinfo("Encryption key required", "Please enter encryption key before selecting a file.")


def open_image():
	# check whether a password has been entered
	if ( passwd.get() ):

		# open window to choose the desired file
		filename = askopenfilename()

		# extract the file name and its extension
		infile, file_extension = os.path.splitext(filename)

		# it will decrypt the file if its extension is .cryptopics
		if( file_extension == ".cryptopics" ):
			decrypt( filename, passwd.get() )
		# otherwise it will encrypt
		else:
			encrypt( filename, passwd.get() )

	# if no pwd, then show pop-up message
	else:
		print_no_pwd_msg()


def encrypt(filename, password):

	# append ".cryptopics" to the encrypted file name that will be created
	outfile = filename + ".cryptopics"
        outfilename = outfile

	# create a 32 byte long random salt
	salt = Random.new().read( KEY_SIZE )

	kdf = PBKDF2(password, salt, ITERATIONS, HASH)

	# the key created by the kdf will be used to encrypt the data
	key = kdf.read( KEY_SIZE )

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
        tkMessageBox.showinfo("Success", "Image encrypted to file: " + outfilename)
        passwd.delete(0,END)


def decrypt(filename, password):

	# extract the file name and its extension
	outfile, file_extension = os.path.splitext(filename)

	# since we only decrypt ".cryptopics" extension, it needs to extract the file extension twice
	outfile, file_extension = os.path.splitext(outfile)

	# appends "_decrypted" to the name of the original file
	outfile = outfile + "_decrypted" + file_extension
        outfilename = outfile

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
        tkMessageBox.showinfo("Success", "Image decrypted to file: " + outfilename)
        passwd.delete(0,END)

# initialize the GUI
root = Tk()

# set the title of the window
root.title("CryptoPics - Python Image Encrypter")

# set the size of the window
window = Frame(root, width=720, height=228, background='white')
window.pack_propagate(0)
window.pack()

img = ImageTk.PhotoImage(file='res/logo.png')
label = Label(window, image=img, borderwidth=0, relief="groove")
label.pack()

passwdLabel = Label(window, text="Enter encryption key to encrypt/decrypt image:", bg='white')
passwdLabel.pack()

passwd = Entry(window, show="*", width=30)
passwd.pack()

# select image button
selectImg = Button(window, text="Select Image", command=open_image)
selectImg.pack(pady=4)

# quit button
quit = Button(window, text="Quit", command=window.quit)
quit.pack({"side": "bottom"}, pady=10)

# instantiate the application
root.mainloop()

```

