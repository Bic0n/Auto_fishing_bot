from functions import *
from InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
import cv2
import numpy as np
import pyperclip as clipboard
import os
from private import *

class Bot:

      def __init__(self, autohot_py, stroke):
        self.autohot_py = autohot_py
        self.stroke = stroke
        self.step = 0
        self.window_info = get_window_info()
        self.useless_steps = 0

      def fishing(self): # start fishing skill
         """self.autohot_py.F11.press()  Enable Shots
         time.sleep(uniform(0.2,0.9))"""
         self.autohot_py.F1.press()

      def reeling(self): # use it when bar moves 
         self.autohot_py.F2.press()

      def pumping(self): # use it when bar DOESNT move 
         self.autohot_py.F3.press()

      def attack_monster(self): # attack spawned monster
         self.autohot_py.F4.press()

      def self_buff(self):
         self.autohot_py.F5.press()

      def get_fishing_bar(self,):

            
            window_info = get_window_info()
            
            img = get_screen(24,386,250,394)          

            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv_color1 = np.asarray([80, 0, 0])   
            hsv_color2 = np.asarray([180, 255, 255])
            mask = cv2.inRange(img_hsv, hsv_color1, hsv_color2)
            mask = np.asarray(mask, dtype = 'int32')
            #cv2.imwrite('{}Mask.jpg'.format(num), mask)
            #cv2.imwrite('{}HSV.jpg'.format(num), img_hsv)

            return np.floor_divide(mask, 255)
      
      def bar_percent(self, bar):


         #bar = self.get_fishing_bar()
         bar = bar[5]


         percent_1 = 1
         for i in range(0,len(bar)-1):
            if bar[i] == bar[i+1]:
               percent_1 += 1
            else:
               break

         percent_2 = 1
         for i in reversed(range(0,len(bar)-1)):
            if bar[i] == bar[i+1]:
               percent_2 += 1
            else:
               break
         #print(round((percent_1 + percent_2)/len(bar),2)*100)
         return round((percent_1 + percent_2)/len(bar),2)*100

      def load_game(self):
            
         os.startfile("C:\Program Files\Asterios\Asterios.exe")
         time.sleep(30)
         self.stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
         self.autohot_py.sendToDefaultMouse(self.stroke)
         time.sleep(1)
         self.stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
         self.autohot_py.sendToDefaultMouse(self.stroke)
         time.sleep(2)
         self.stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
         self.autohot_py.sendToDefaultMouse(self.stroke)
         time.sleep(1)
         self.stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
         self.autohot_py.sendToDefaultMouse(self.stroke)
         time.sleep(2)
         self.autohot_py.ENTER.press()
         time.sleep(55)


         clipboard.copy(private.username)
         self.autohot_py.RIGHT_CTRL.down()
         self.autohot_py.V.down()
         self.autohot_py.RIGHT_CTRL.up()
         self.autohot_py.V.up()
         time.sleep(3)

         self.autohot_py.TAB.press()

         time.sleep(1)
         clipboard.copy(private.password)
         self.autohot_py.RIGHT_CTRL.down()
         self.autohot_py.V.down()
         self.autohot_py.RIGHT_CTRL.up()
         self.autohot_py.V.up()

         time.sleep(1)
         self.autohot_py.ENTER.press()

         time.sleep(3)
         self.autohot_py.ENTER.press()

         time.sleep(3)
         self.autohot_py.ENTER.press()

         time.sleep(3)
         self.autohot_py.ENTER.press()

      def fishing_position(self):
         self.autohot_py.F5.press()
         time.sleep(1)
         self.autohot_py.ESC.press()
