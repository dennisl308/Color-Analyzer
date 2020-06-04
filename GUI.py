# imported libaries
from tkinter import *

# create root window
root = Tk()
root.geometry('600x300') # width x height

l = Label(root, text="Hello World!") # create element
l.pack() # add element to root window

# maintain presence of root window
root.mainloop()