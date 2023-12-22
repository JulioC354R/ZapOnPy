
import ctypes
import logging
import time
import keyboard
import pyautogui


class Config:
    def __init__(self) -> None:
        pass
    
    def turn_off_num_lock(self):
        # 0x90 é o código da tecla Num Lock
        num_lock_on = ctypes.windll.user32.GetKeyState(0x90) & 1
        if num_lock_on:
            pyautogui.press('numlock')
            logging.info('Desligando Num Lock.')
    
        
    def stop(self, stop_condition = bool):
        if keyboard.is_pressed('F5'):
            stop_condition = True
            logging.warning('O Código foi parado, tecla "F5" pressionada.')
        return stop_condition
    
    def open_whatsapp(self):
        pyautogui.press('win')
        time.sleep(0.2)
        pyautogui.write('whatsapp')
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(6)
        logging.info('Whatsapp aberto.')