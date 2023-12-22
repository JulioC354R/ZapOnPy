import webbrowser
import pyautogui
import time
import pyperclip
import os
import logging
from mouse import Mouse
from config import Config


# Exemplo de mensagens de log
#logging.debug('Isso é uma mensagem de depuração.')
##logging.info('Isso é uma mensagem informativa.')
#logging.warning('Isso é uma mensagem de aviso.')
#logging.error('Isso é uma mensagem de erro.')
#logging.critical('Isso é uma mensagem crítica.')


class Message:

    def __init__(self) -> None:
        pass

    def check_new_message(self, region = list):
        '''Checa se possui o ícone de mensagens novas na região
        e clica nele, retorna True se encontrar, False caso contrário.'''
        
        x_r, y_r, w_r, h_r = region

        for image in Mouse.new_messages_icons:
            try:
                # Tenta localizar e clicar na imagem
                new_message = pyautogui.locateCenterOnScreen(image, confidence=0.7, region=(x_r, y_r, w_r, h_r))
                #tirar o is true
                if new_message:
                    logging.info(f'Imagem localizada: {image}.')
                    # Se encontrou a imagem, clica e retorna True
                    pyautogui.click(new_message.x, new_message.y)
                    return True
            except pyautogui.ImageNotFoundException:
                # Se a imagem não foi encontrada, continua para a próxima
                logging.info(f'Imagem {image} não encontrada.')

        # Se nenhuma imagem foi encontrada, retorna False
        return False

            

    def get_message(self):
        logging.info('Pegando a mensagem.')
        Config.turn_off_num_lock(self)
        try:
            for i in range(3):
                pyautogui.hotkey('shift' ,'tab')
                time.sleep(0.1)
            pyautogui.press('end')
            time.sleep(0.1)
            pyautogui.press('apps')
            time.sleep(0.5)
            for i in range(3): 
                pyautogui.press('down')
                time.sleep(0.1)
            pyautogui.press('enter')
            message = pyperclip.paste()
            logging.debug(f'Mensagem copiada: {message}.')
            return message
        except Exception as e:
            logging.error(f'Erro ao pegar a mensagem: {e}.')
            return None
        
    def send_message_on_chat(self, message = str, get_out = True, search_image = True):
        '''Envia mensagem com o chat aberto'''
        #clica na aba de escrever
        logging.info('Enviando mensagem no chat...')
        #procurar a imagem ou clicar no lugar padrão baseado nas resoluções compatíveis
        if search_image:
            Mouse.click_on_image(self, Mouse.message_box)
        else:
            Mouse.click_on_Message_box(self)
        time.sleep(0.5)
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        logging.info(f'Enviou a mensagem: {message}')
        if get_out == True:
            pyautogui.hotkey('ctrl', 'w')

    def send_image_on_chat(self, image_path = str, message =str, get_out = True, search_image = True):
        '''Enquanto a conversa está open:
        abre uma imagem com o caminho, copia ela, cola no whatsapp
        cola a mensagem, envia ao contato, volta para a imagem e fecha.'''
        
        #abrindo e copiando a imagem
        # Usa o visualizador de imagens padrão do sistema operacional

        os.startfile(image_path)
        logging.debug(f'Abrindo imagem {image_path}.')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        #voltando e fechando a imagem
        pyautogui.press('esc')
        logging.debug('Imagem fechada.')
        time.sleep(0.1)
        #clica na aba de escrever
        if search_image:
            Mouse.click_on_image(self, Mouse.message_box)
        else:
            Mouse.click_on_Message_box(self)
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        logging.debug(f'Escreveu a mensagem: {message}')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        if get_out:
            pyautogui.hotkey('ctrl', 'w')
        logging.info(f'Imagem enviada {image_path}')




    def send_poll(self, question=str, multiple_responses = False, get_out = True, search_image = True, *args):
        '''Escreve uma enquete, ela pode ter ou não multiplas respostas.'''
        if search_image:
            Mouse.click_on_image(self, Mouse.message_box)
        else:
            Mouse.click_on_Message_box(self)

        pyautogui.hotkey('shift', 'tab')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('up')
        pyautogui.press('up')
        time.sleep(0.1)
        pyautogui.press('enter')
        pyperclip.copy(question)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        logging.debug(f'Escreveu a pergunta: {question}')
        pyautogui.press('tab')
        time.sleep(0.1)
        for option in args:
            pyperclip.copy(option)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            pyautogui.press('down')
            time.sleep(0.1)
            logging.debug(f'Escreveu a opcao: {option}.')
        pyautogui.press('tab')
        time.sleep(0.1)
        if multiple_responses == False:
            pyautogui.press('space')
            time.sleep(0.1)
        pyautogui.press('tab')
        time.sleep(0.1)
        pyautogui.press('space')
        logging.info(f'A enquete {question} foi enviada.')
        time.sleep(1)

        Mouse.click_on_Message_box(self)
        if get_out == True:
            pyautogui.hotkey('ctrl', 'w')


    def send_direct_message(self, number, text, get_out = True, search_image = True):
        link = f'https://api.whatsapp.com/send?phone={number}'
        logging.debug(f'abrindo o link: {link}')
        webbrowser.open(link)
        time.sleep(3)
        if search_image:
            Mouse.click_on_image(self, Mouse.message_box)
        else:
            Mouse.click_on_Message_box(self)
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        logging.info(f'Mensagem enviada: {text}')
        time.sleep(1)
        if get_out == True:
            pyautogui.hotkey('ctrl', 'w')

    def search_chat(self, contatc_or_group = str, search_image = True):
        '''Procura pelo nome o contato/grupo e clica nele, essa função retorna outra função
        que pode ser utilizado para limpar a barra de pesquisa depois de sair do chat'''

        if search_image:
            Mouse.click_on_image(self, Mouse.search_box)
        else:
            Mouse.click_on_search_box(self)
        pyperclip.copy(contatc_or_group)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('tab')
        pyautogui.press('enter')
        
        def clean_search(self, search_image = True):

            #clicar onde pesquisa a conversa
            if search_image:
                Mouse.click_on_image(self, Mouse.search_box)
            else:
                Mouse.click_on_search_box(self)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('del')

        return clean_search






         