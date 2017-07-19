# CryptoPics

**Prerequisites**  
  Python >2.7  

```
root@kali:~# python --version 
Python 2.7.13
```

**Dependancies**  
Python Modules 
  * pycrypto  
  * tkinter  
  * pillow  

All dependancies needed to run the project are already preinstalled on Kali Linux.

Clone the Git repo: 

```
root@kali:~# git clone https://github.com/cahlen/IMEncrypt.git
```

Run the program: 

``` 
root@kali:~# cd cryptopics
root@kali:~# python ./imencrypt.py
```
Python Code

```python
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
```

