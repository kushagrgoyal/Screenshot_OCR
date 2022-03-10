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
        img_lines = copy.deepcopy(img) # Copying the image in a duplicate variable name
        
        # Creating a cv2 window and setting full-screen property to it
        cv2.namedWindow('Screenshot', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Screenshot', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # cv2.imshow('Screenshot', img)

        
        # def mouse_move(event):
        #     if event == cv2.EVENT_MOUSEMOVE:
        #         while True:
        #             # Horizontal line
        #             cv2.line(img_lines, (0, pyautogui.position()[1]), (size_x, pyautogui.position()[1]), (0, 255, 0), 1)

        #             # Vertical Line
        #             cv2.line(img_lines, (pyautogui.position()[0], 0), (pyautogui.position()[0], size_y), (0, 255, 0), 1)

        #             cv2.imshow('Screenshot', img_lines)
        #             img_lines = img

        #             if cv2.waitKey(1) & 0xFF == ord('q'):
        #                 break
                
        #         cv2.destroyAllWindows()

        # # bind the callback function to window
        # cv2.setMouseCallback('Screenshot', mouse_move())
        
        # Getting screen size
        # 1920*1080 for current screen
        size_x, size_y = pyautogui.size()
        
        while True:
            # Horizontal line
            cv2.line(img_lines, (0, pyautogui.position()[1]), (size_x, pyautogui.position()[1]), (0, 255, 0), 1)

            # Vertical Line
            cv2.line(img_lines, (pyautogui.position()[0], 0), (pyautogui.position()[0], size_y), (0, 255, 0), 1)

            cv2.imshow('Screenshot', img_lines)
            img_lines = copy.deepcopy(img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()


app = qtw.QApplication([])
mw = MainWindow()
# mw.show()

# Run the app
app.exec()