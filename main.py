from ZapOnPy import ZOP
from commandos import Comandos
import logging
import time

logging.basicConfig(
    filename='BotAutoPy.log',  # Nome do arquivo de log
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

bot = ZOP(True, False)
comm = Comandos(bot)

while True:

    new_messages = bot.check_new_messages()

    if new_messages is not None:
        print(new_messages)
        last_msg = bot.get_last_message()
        print(last_msg)

        comm.check_command(last_msg)
        # chat_type, number = bot.get_number()
        # bot.send_message_on_chat(f'Numero encontrado: {number}', False)
        # bot.send_message_on_chat(f'Tipo de chat: {chat_type}')

        bot.close_chat()
