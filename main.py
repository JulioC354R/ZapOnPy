from ZapOnPy import ZOP
from commandos import Comandos
import logging
import time
from options import *

logging.basicConfig(
    filename='BotAutoPy.log',  # Nome do arquivo de log
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

bot = ZOP(True, False)
comm = Comandos(bot)

while True:

    time.sleep(2)
    bot.search_contact("Julio Developer")
    list_out = bot.find_messages(Msg_options.OUT)
    list_in = bot.find_messages(Msg_options.IN)
    list_all = bot.find_messages(Msg_options.ALL)
    print(list_out)
    print(list_in)
    print(list_all)
    last_message_out = bot.get_messages(Msg_options.OUT)[-1]
    complete = bot.find_message_complete_element(last_message_out)
    bot.react_a_message(complete, React_options.HEART)
    time.sleep(0.5)
    bot.send_file_in_input(
        Input_options.DOCUMENT, r"C:\Users\julyo\Music\[AMV] Kizumonogatari - Castle(MP3_160K).mp3", "Se liga no som")
    bot.close_chat()
    # campo = bot.find_field(Field_options.MESSAGE)
    # time.sleep(1)
    # campo.send_keys("Favoritado", Keys.ENTER)

    time.sleep(50)
