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

        # Add a title
        self.setWindowTitle('Screenshot OCR')

        # Set a vertical Layout
        self.setLayout(qtw.QVBoxLayout())

        # Create a label
        my_label = qtw.QLabel('Use a box to select the area to extract text out of')
        my_label.setFont(qtg.QFont('Helvetica', pointSize = 14))
        self.layout().addWidget(my_label)

        # Create a button
        ss = qtw.QPushButton('Screenshot', clicked = lambda: self.click_button())
        self.layout().addWidget(ss)

        # Show the app
        self.show()

    def click_button(self):
        '''
        This function takes the screenshot and displays it, currently.
        '''
        self.hide()
        time.sleep(0.2)
        img = pyautogui.screenshot()
        self.show()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Creating a cv2 window and setting full-screen property to it
        cv2.namedWindow('Screenshot', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Screenshot', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Screenshot', img)

        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()


app = qtw.QApplication([])
mw = MainWindow()
# mw.show()

# Run the app
app.exec()