# CryptoPics

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
  * pillow  

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

