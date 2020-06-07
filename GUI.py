# Graphical User Interface for Color Analyzer

# Imported libaries
import sys, os # argv, exit status
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSplitter, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

from tkinter import *
from PIL import ImageTk, Image

# Design of the area where an image can be dragged and dropped into
#   Inherits QLabel
class ImageLabel(QLabel):
    # Class initializer
    def __init__(self):
        super().__init__()  # Initialize QLabel (0 parameters)

        # Image border using CSS
        self.setStyleSheet('''
            QLabel{
                border: 5px solid #a9a9a9
            }
        ''')
        self.setAlignment(Qt.AlignCenter)   # Align inside contents to the center
        self.setText('<font size=5>Drop Image Here</font>')
        self.setGeometry(0, 0, 500, 500)

    # Display image, maintain aspect ratio
    def setPixmap(self, image):
        size = self.size() # get image size
        size = size * 0.90  # shrink size to avoid touching border
        super().setPixmap(QPixmap(image).scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)) # set/change image properties

# Application Window
#   Inherits QWidget
class Application(QWidget):
    # Class initializer
    def __init__(self):
        super().__init__()  # Initialize QWidget (0 parameters)

        # Application properties
        self.setWindowTitle('Dominant Color Analyzer')  # Application title
        self.setWindowIcon(QIcon('./images/ColorAnalyzer.ico')) # Application icon
        self.setFixedSize(1000, 500) # Fixed application size (W x H)
        self.setAcceptDrops(True) # allow outside signals (images)

        #
        # <--
        mainSplit = QSplitter(Qt.Horizontal) # align panels horizontally

        # Drag-and-drop Widget
        self.photoViewer = ImageLabel() # instantiate class
        mainSplit.addWidget(self.photoViewer)  # add widget

        # Right-side Widget
        rightSide = QFrame()    # create frame
        rightSide.setFrameShape(QFrame.StyledPanel) # set style
        mainSplit.addWidget(rightSide)   # add widget

        # Customize main split
        mainSplit.setSizes([500, 500]) # size
        
        # Main layout
        mainLayout = QHBoxLayout()  # initialize object to add widgets to the layout
        mainLayout.addWidget(mainSplit) # add splitter to laybout
        self.setLayout(mainLayout)  # invoke layout manager (first paramater) for positioning
        # -->
        #

    # Event handler called when a file is dragged with the mouse into the widget
    def dragEnterEvent(self, event):
        # accept if file is an image, otherwise ignore it
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
    
    # Event handler called when a drag is in progress
    def dragMoveEvent(self, event):
        # accept if file is an image, otherwise ignore it
        if event.mimeData().hasImage and event.answerRect().intersects(ImageLabel().geometry()):  ## fix this
            event.accept()
        else:
            event.ignore()

    # Event handler called when the drag is dropped into the widget
    def dropEvent(self, event):
        # accept if file is an image, otherwise ignore it
        #   before accepting, get file address and display image
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)  # recieve copy of the data dropped in
            file_path = event.mimeData().urls()[0].toLocalFile()    # store directory address of file
            self.set_image(file_path)
            event.accept()
        else:
            event.ignore()

    # Display image from given file path
    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))

## <--
app = QApplication(sys.argv) # create instance (GUI application control flow manager)

demo = Application() # create object for the application
demo.show() # show application

sys.exit(app.exec_())   # run application's event loop (main loop)
## -->

'''
# create root window
root = Tk()
root.geometry('900x600') # width x height
root.resizable(width=False, height=False)

# background image
bgImage = PhotoImage(file="./images/red.png")
bgLabel = Label(root, image = bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

l = Label(root, text="Hello World!") # create element
l.pack() # add element to root window

# maintain presence of root window
root.mainloop()
'''