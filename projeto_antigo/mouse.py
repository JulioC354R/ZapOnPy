import logging
import time
import pyautogui

class Mouse:
    new_messages_icons = ['images/new_message_icon.png', 'images/new_message_icon_2.png','images/new_message_icon_3.png']
    DM_button   = ['images/send_icon.png', 'images/send_icon_2.png', 'images/send_icon_3.png']
    message_box = ['images/message_box.png', 'images/message_box2.png', 'images/message_box3.png','images/message_box4.png']
    search_box    = ['images/search_chat.png', 'images/search_chat_2.png', 'images/search_chat_3.png','images/search_chat4.png']

    def get_new_messages_region(self):
        # Area de novas mensagens
        screen_resolution = pyautogui.size()
        logging.info(f'Tamanho de tela definido: {screen_resolution[0]} x {screen_resolution[1]}')
        match screen_resolution:
            case (1920,1080):
                return [364, 171, 52, 841]
            case (1024,768):
                return [250, 150, 130, 570]
            case (800,600):
                return [200, 154, 251, 235]

    def click_on_Message_box(self):
        screen_width, screen_height = pyautogui.size()
        resolution = [screen_width, screen_height]
        match resolution:
            case [800,600]:
                pyautogui.click(x=454, y=535)
            case [1024,768]:
                pyautogui.click(x=594, y=694)
            case [1920,1080]:
                pyautogui.click(x=679, y=1002)



    def click_on_search_box(self, resolution):
        screen_width, screen_height = pyautogui.size()
        resolution = [screen_width, screen_height]
        match resolution:
            case [800,600]:
                pyautogui.click(x=163, y=115)
            case [1024,768]:
                pyautogui.click(x=161, y=113)
            case [1920,1080]:
                pyautogui.click(x=166, y=115)

    def click_on_image(self, image_paths = list):
        for image in image_paths:
            try:
                click = pyautogui.locateCenterOnScreen(image, confidence= 0.7)
                pyautogui.click(click.x, click.y)
                time.sleep(0.2)
                logging.debug(f'Clicando na imagem {image}')
                break
            except:
                logging.info(f'Imagem não encontrada: {image}')