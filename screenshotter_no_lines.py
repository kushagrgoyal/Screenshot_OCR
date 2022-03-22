import copy
import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import time


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # Declaring variables for use later on during rectangle drawing for selection
        self.ix = -1
        self.iy = -1
        self.drawing = False
        self.img2 = None
        self.done = False

        # Add a title
        self.setWindowTitle('Screenshot OCR')

        # Set a vertical Layout
        self.setLayout(qtw.QVBoxLayout())

        # Create a top label
        my_label = qtw.QLabel('Use a box to select the area to extract text out of')
        my_label.setFont(qtg.QFont('Helvetica', pointSize = 14))
        self.layout().addWidget(my_label)

        # Create a button
        ss = qtw.QPushButton('Screenshot', clicked = lambda: self.click_button())
        self.layout().addWidget(ss)

        # Create a bottom label
        bot_label = qtw.QLabel('Press Q to exit from screenshot model after clicking the button')
        bot_label.setFont(qtg.QFont('Helvetica', pointSize = 12))
        self.layout().addWidget(bot_label)

        # Creating area for the image captured by the screenshotter
        ss = qtg.QPixmap(self.img2)
        ss_label = qtw.QLabel()
        ss_label.setPixmap(ss)
        ss_label.setHidden(self.done)
        self.layout().addWidget(ss_label)

        # Show the app
        self.show()

    def click_button(self):
        '''
        This function takes the screenshot and displays it, currently.
        '''
        self.done = False
        self.hide()
        time.sleep(0.2)
        self.img = pyautogui.screenshot()
        self.show()
        self.img = cv2.cvtColor(np.array(self.img), cv2.COLOR_RGB2BGR)
        self.img2 = copy.deepcopy(self.img)
        
        # Creating a cv2 window and setting full-screen property to it
        cv2.namedWindow('Screenshot', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Screenshot', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)        

        def draw_rectangle(event, x, y, flags, param):
            '''
            This function is used to create a rectangle to show the selection for the crop area
            - Mouse Callback function outputs 5 params, hence this function takes 5 parameters as inputs
            '''
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.ix = x
                self.iy = y

            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing == True:
                    self.img2 = copy.deepcopy(self.img)
                    cv2.rectangle(self.img2, pt1 = (self.ix, self.iy), pt2 = (x, y), color = (255, 255, 255), thickness = 1)

            elif event == cv2.EVENT_LBUTTONUP:
                self.drawing = False
                self.img2 = copy.deepcopy(self.img)
                cv2.rectangle(self.img2, pt1 = (self.ix, self.iy), pt2 = (x, y), color = (255, 255, 255), thickness = 1)
                self.img2 = self.img[self.iy:y, self.ix:x]

                # This will destroy the original window and only show the updated window with the cropped selection
                cv2.destroyAllWindows()
                self.done = True


        # Bind the callback function to window
        cv2.setMouseCallback('Screenshot', draw_rectangle)
        
        while True:
            cv2.imshow('Screenshot', self.img2)
            
            if cv2.waitKey(1) & 0xFF == ord('q') or self.done == True:
                # cv2.imwrite('./temp.png', self.img2)
                break
        
        cv2.destroyAllWindows()


app = qtw.QApplication([])
mw = MainWindow()
# mw.show()

# Run the app
app.exec()