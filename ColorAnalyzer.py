# Graphical User Interface for Color Analyzer

# Imported libaries
import sys, os # argv, exit status
import pyautogui # size(), position(), screenshot()
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGroupBox, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QFont

# Check if file is an image format accepted by QPixmap
def verifyImage(file_path):
    if file_path.lower().endswith(('.bmp', '.gif', '.jpg', '.jpeg', '.png', '.pbm', '.pgm', '.ppm', '.xbm', '.xpm')):
        return True
    else:
        # Pop-up error message
        messageError = QMessageBox()
        messageError.setText("Invalid file type.")
        messageError.exec()
        return False

# Design of the widget where an image can be dragged and dropped into (Inherits QLabel)
class ImageLabel(QLabel):
    # Class initializer
    def __init__(self):
        super().__init__()  # Initialize QLabel (0 parameters)

        # Image label properties
        self.setAlignment(Qt.AlignCenter)   # Align inside contents to the center
        self.setGeometry(0, 0, 500, 500)
        self.setFont(QFont('Arial', 15))
        self.setText('Drop Image Here')

        # Image label border using CSS
        self.setStyleSheet('''
            QLabel{
                border: 5px solid #a9a9a9
            }
        ''')

    # Display drag-n-drop image
    def setPixmap(self, image):
        size = self.size() * 0.90  # shrink image size to avoid touching border
        super().setPixmap(QPixmap(image).scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)) # keep aspect ratio

    # Reset/clear image label
    def clearImage(self):
        self.setText('Drop Image Here')

# Right widget (Inherits QGroupBox)
class DetailsLabel(QGroupBox):
    def __init__(self):
        super().__init__("Image Details")   # widget title

# Application Window (Inherits QWidget)
class Application(QWidget):
    # Placeholders, default values
    r, g, b = 0, 0, 0   # RGB variables
    file_name = ""      # filename
    file_path = ""      # filepath

    # Class initializer
    def __init__(self):
        super().__init__()  # Initialize QWidget (0 parameters)

        # Application properties
        self.setWindowTitle('Dominant Color Analyzer')  # Application title
        self.setWindowIcon(QIcon('./images/ColorAnalyzer.ico')) # Application icon
        self.setFixedSize(1000, 500) # Fixed application size (W x H)
        self.setAcceptDrops(True) # allow outside signals (images)

        mainSplit = QGridLayout()   # instantiate grid layout

        # Drag-and-drop widget
        self.photoViewer = ImageLabel() # instantiate class
        mainSplit.addWidget(self.photoViewer, 0, 0)  # add widget

        # Details widget
        self.detailViewer = DetailsLabel()
        mainSplit.addWidget(self.detailViewer, 0, 1)
        
        self.setLayout(mainSplit)   # set layout

        # Filepath label properties (detail widget area)
        self.label_FilePath = QLabel(self)
        self.label_FilePath.setText("File Name:\nFile Path:\n")
        self.label_FilePath.setGeometry(QRect(525, 0, 440, 185))
        self.label_FilePath.setFont(QFont('Arial', 11))
        self.label_FilePath.setWordWrap(True)   # new line if text goes out of bounds

        # RGB label properties (detail widget area)
        self.label_RGB = QLabel(self)
        hex = '%02x%02x%02x' % (self.r, self.g, self.b) 
        self.label_RGB.setText('Decimal Code: RGB({},{},{})\n#{}'.format(self.r, self.g, self.b, hex))
        self.label_RGB.setGeometry(QRect(525, 0, 440, 350))
        self.label_RGB.setFont(QFont('Arial', 11))
        self.label_RGB.setWordWrap(True)
    
    # Event handler called when a file is initially dragged into the widget
    def dragEnterEvent(self, event):
        event.accept()

    # Event handler called when a drag is in progress
    def dragMoveEvent(self, event):
        # Ensure you can only drop in the drag-n-drop window area
        if event.answerRect().intersects(ImageLabel().geometry()):
            event.accept()
        else:
            event.ignore()
    
    # Event handler called when the drag is dropped into the widget
    def dropEvent(self, event):
        self.file_path = event.mimeData().urls()[0].toLocalFile()   # store directory address of file
        self.file_name = os.path.basename(self.file_path)   # get filename
        self.label_FilePath.setText("File Name: {}\nFile Path: {}\n".format(self.file_name, self.file_path))    # print file properties

        # Accept if file is an image, otherwise ignore it
        if verifyImage(self.file_path):
            self.photoViewer.setPixmap(QPixmap(self.file_path))  # generate image
            event.accept()
        else:
            self.photoViewer.clearImage()   # reset image label
            event.ignore()

    # Event handler called when a mouse click occurs
    def mousePressEvent(self, event):
        mouse_x_position, mouse_y_position = pyautogui.position()   # get mouse x and y positions
        pixel = pyautogui.screenshot(region = (mouse_x_position, mouse_y_position, 1, 1)).convert('RGB').getcolors()    # get pixel RGB color based on mouse position
        self.r, self.g, self.b = pixel[0][1]   # get specific RGB values from pixel
        hex = '%02x%02x%02x' % (self.r, self.g, self.b) # rgb to hex
        self.label_RGB.setText('Decimal Code: RGB({},{},{})\n#{}'.format(self.r, self.g, self.b, hex))  # print rgb and hex
        self.update() # update color displayed

    # Event handler called when color needs to be displayed
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    # Display color that was clicked
    def drawRectangles(self, qp):
        qp.setBrush(QColor(self.r, self.g, self.b))
        qp.drawRect(520, 215, 450, 250) # position and size (x,y,w,h)

app = QApplication(sys.argv)    # create instance (GUI application control flow manager)
demo = Application()            # create object for the application
demo.show()                     # show application
sys.exit(app.exec_())           # run application's event loop (main loop)

# getcolors() gets rgb values of whole picture