import pyautogui
import time
from mensagem import Message
from comandos import Commands
from mouse import Mouse
from config import Config
import logging

# Configurar o logging para escrever em um arquivo
logging.basicConfig(
    filename='BotAutoPy.log',  # Nome do arquivo de log
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#Ao colocar false procura menos imagens, apenas as novas mensagens.
#Para isso a janela deve estar em tela cheia.
search_all_images = False

mensagem = Message()
command = Commands()
mouse = Mouse()
config = Config()

config.open_whatsapp()

region_new_messages = mouse.get_new_messages_region()
logging.debug(f'Definindo região de novas mensagens: {region_new_messages}')

msg_recebida = ""
loop = True
stop_condition = False
while loop and stop_condition == False:
    #desliga o num lock se tiver ativado
    config.turn_off_num_lock()

    # Condição de parada, se pressionar F5 parar o código:
    stop_condition = config.stop(stop_condition)
    # Localizar e ícone de nova mensagem apenas na região específica
    if stop_condition is False:    
        try:
            logging.info('Checando novas mensagens.')
            novas_mensagens = mensagem.check_new_message(region_new_messages)
            logging.info(f'Novas mensagens: {novas_mensagens}')
            time.sleep(1)
        
            if novas_mensagens is True:
                msg_recebida = mensagem.get_message()
                                                                                    
            time.sleep(1)

            if msg_recebida == '!teste' and novas_mensagens:
                logging.info('Executando comando: !teste.')
                command.test(search_all_images)
            if msg_recebida == '!apresentar' and novas_mensagens:
                logging.info('Executando comando: !apresentar.')
                command.apresentation()
            if msg_recebida == '!enquete' and novas_mensagens:
                logging.info('Executando comando: !enquete')
                command.poll()
            if '!sendDM' in msg_recebida and novas_mensagens:
                logging.info('Executando comando: !sendDM.')
                command.send_DM_to(msg_recebida)
            if '!help' in msg_recebida and novas_mensagens:
                logging.info('Executando comando: !help. ')
                command.help(msg_recebida)
            if '!ficha' in msg_recebida and novas_mensagens:
                logging.info('Executando comando: !ficha. ')
                command.ficha(msg_recebida)
            if '!dados player' in msg_recebida and novas_mensagens:
                logging.info('Executando comando: !mostrar. ')
                command.mostrar_dados(msg_recebida)
            else:
                logging.info('Comando não reconhecido.')
                pyautogui.hotkey('ctrl', 'w')
                logging.debug('Conversa Fechada.')
            
        except pyautogui.ImageNotFoundException as e:
            logging.info(f'Não há novas mensagens: {e}')
            pyautogui.press('esc')
            logging.debug('Botão pressionado: "esc".')
            stop_condition = config.stop(stop_condition)
            time.sleep(1)
        except Exception as e:
            logging.error(f'Ocorreu um erro: {e}')
            logging.shutdown()
            stop_condition = config.stop(stop_condition)
            time.sleep(1)
        time.sleep(1)

logging.shutdown() #fechando o arquivo log