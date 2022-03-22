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
        global img_lines
        img_lines = copy.deepcopy(img) # Copying the image in a duplicate variable name
        
        # Creating a cv2 window and setting full-screen property to it
        cv2.namedWindow('Screenshot', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Screenshot', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # cv2.imshow('Screenshot', img)
        
        # Variable declaration for drawing rectangle
        # global ix, iy, drawing
        ix = -1
        iy = -1
        drawing = False

        def draw_rectangle(event, x, y, flags, param):
            '''
            This function is used to create a rectangle to show the selection for the crop area
            - Mouse Callback function outputs 5 params, hence this function takes 5 parameters as inputs
            '''
            global ix, iy, drawing, img_lines
            drawing = False
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                ix = x
                iy = y

            elif event == cv2.EVENT_MOUSEMOVE:
                # Horizontal line
                cv2.line(img_lines, (0, pyautogui.position()[1]), (size_x, pyautogui.position()[1]), (0, 255, 0), 1)

                # Vertical Line
                cv2.line(img_lines, (pyautogui.position()[0], 0), (pyautogui.position()[0], size_y), (0, 255, 0), 1)

                if drawing == True:
                    cv2.rectangle(img_lines, pt1 = (ix, iy), pt2 = (x, y), color = (0, 255, 255), thickness = 4)
                    # img_lines = copy.deepcopy(img)

            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False
                cv2.rectangle(img_lines, pt1 = (ix, iy), pt2 = (x, y), color = (0, 255, 255), thickness = 4)
                # img_lines = copy.deepcopy(img)


        # Bind the callback function to window
        cv2.setMouseCallback('Screenshot', draw_rectangle)
        
        # Getting screen size
        # 1920*1080 for current screen
        size_x, size_y = pyautogui.size()
        
        while True:
            # # Horizontal line
            # cv2.line(img_lines, (0, pyautogui.position()[1]), (size_x, pyautogui.position()[1]), (0, 255, 0), 1)

            # # Vertical Line
            # cv2.line(img_lines, (pyautogui.position()[0], 0), (pyautogui.position()[0], size_y), (0, 255, 0), 1)

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