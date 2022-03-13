from AutoHotPy.AutoHotPy import AutoHotPy
from InterceptionWrapper import InterceptionMouseState,InterceptionMouseStroke
from functions import *
from bot import Bot
import time
import random
import win32gui
import win32api
import numpy as np
import requests
import private

if __name__ == "__main__":

     auto = AutoHotPy()
     stroke = InterceptionMouseStroke()
     bot = Bot(auto, stroke)
     
     
     delay = 0.9
     num = 0
     t = 25
     time.sleep(4)

     while True:
          
          if CheckIfWindowCrash(): # Crash error 
               url='https://api.telegram.org/bot'+str(private.API)+'/sendMessage?text='+str('Crit Error')+'&chat_id='+str(private.chat_id) #  
               response = requests.get(url)
               time.sleep(2)
               id = CheckIfWindowCrash()
               win32gui.EnableWindow(id, True)
               #win32gui.SetForegroundWindow(id)
               (left, top, right, bottom) = win32gui.GetWindowRect(id)
               auto.moveMouseToPosition(right-50,bottom-15)
               
               stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
               auto.sendToDefaultMouse(stroke)
               time.sleep(0.5)
               stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
               auto.sendToDefaultMouse(stroke)
               time.sleep(15)
               print(checkIfProcessRunning())
               if not checkIfProcessRunning():
                    bot.load_game()
                    time.sleep(10)
                    bot.fishing_position()
                    time.sleep(5)
                    continue
          
 
          fishing_bar = bot.get_fishing_bar()
          time.sleep(1.2)
          bot.attack_monster()
          if bot.bar_percent(fishing_bar) != 100:
               if t != time.localtime().tm_hour:
                    auto.F5.press() # Use white bottle every hour
                    t = time.localtime().tm_hour
               bot.pumping()
               bot.fishing()
               
               #print("Start Fishing")
               time.sleep(2)
               bot.attack_monster()
               time.sleep(13)
               index = 0
               while bot.bar_percent(bot.get_fishing_bar()) != 100 and index < 13:
                    time.sleep(1)
                    index += 1
               continue

          fishing_bar2 = bot.get_fishing_bar()
          if np.sum(fishing_bar2[3:6]) < np.sum(fishing_bar[3:6]):  # Check if bar moves or not
               bot.reeling()
               time.sleep(1.1)
          
               if np.sum(fishing_bar2[5]) - np.sum(bot.get_fishing_bar()[5]) > 30: # if wrong detected reeling, use pumping
                    bot.pumping()  
                    time.sleep(delay)
                    continue
               continue
          else:
               bot.pumping()
               time.sleep(1.1)
               if np.sum(fishing_bar2[5]) - np.sum(bot.get_fishing_bar()[5]) > 30: # if wrong detected pumping, use reeling
                    bot.reeling()
                    time.sleep(delay)
                    continue
               continue
