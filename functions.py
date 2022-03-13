import time
import win32gui
from AutoHotPy.AutoHotPy import AutoHotPy
from InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
from random import *
from PIL import ImageOps, Image, ImageGrab
from numpy import *
import time
import cv2
import psutil



WINDOW_SUBSTRING = "Asterios"


def get_window_info():
    # set window info
    window_info = {}
    win32gui.EnumWindows(set_window_coordinates, window_info)
    return window_info

# EnumWindows handler
# sets L2 window coordinates
def set_window_coordinates(hwnd, window_info):
    if win32gui.IsWindowVisible(hwnd):
        if WINDOW_SUBSTRING in win32gui.GetWindowText(hwnd):
            win32gui.ShowWindow(hwnd, 3)
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            window_info['x'] = x
            window_info['y'] = y 
            window_info['width'] = w
            window_info['height'] = h
            window_info['name'] = win32gui.GetWindowText(hwnd)
            #win32gui.SetForegroundWindow(hwnd)


def get_screen(x1, y1, x2, y2):
    
    box = (x1, y1 , x2, y2)
    screen = ImageGrab.grab(box)
    
    img = array(screen.getdata(), dtype=uint8).reshape((screen.size[1], screen.size[0], 3))
    
    return img


def get_target_centers(img):

    # Hide buff line
    # img[0:70, 0:500] = (0, 0, 0)

    # Hide your name in first camera position (default)
    img[210:230, 350:440] = (0, 0, 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('1_gray_img.png', gray)

    # Find only white text
    ret, threshold1 = cv2.threshold(gray, 252, 255, cv2.THRESH_BINARY)
    # cv2.imwrite('2_threshold1_img.png', threshold1)

    # Morphological transformation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 5))
    closed = cv2.morphologyEx(threshold1, cv2.MORPH_CLOSE, kernel)
    # cv2.imwrite('3_morphologyEx_img.png', closed)
    closed = cv2.erode(closed, kernel, iterations=1)
    # cv2.imwrite('4_erode_img.png', closed)
    closed = cv2.dilate(closed, kernel, iterations=1)
    # cv2.imwrite('5_dilate_img.png', closed)

    (_, centers, hierarchy) = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return centers


def get_mouse_position():
     if (auto.A.isPressed() | auto.LEFT_ALT.isPressed()):
          pos = auto.getMousePosition()
          message = "\rMouse is at x: {}, y: {}".format(mouse['x'], mouse['y']) + ' ' * 10
          print(message, end='', flush=True)
          return {'x': pos[0], 'y': pos[1]}


def checkIfProcessRunning(processName = 'Asterios'):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


def CheckIfWindowCrash(window = 'LineageII Crash Report'):
    windows_list = []
    top_list = []
    def enum_win(hand, result):
        win_test = win32gui.GetWindowText(hand)
        windows_list.append((hand, win_test))
    win32gui.EnumWindows(enum_win, top_list)

    for (hwnd, win_text) in windows_list:
        if window in win_text:
            print(win32gui.GetWindowText(hwnd), hwnd)
            return hwnd
    return False
            
            
if __name__ == "__main__":
    info = get_window_info()
    print('Window info:', info)
    time.sleep(3)
    Image.fromarray(get_screen(info['x'],info['y'],info['width'],info['height'])).show()
    




