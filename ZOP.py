from options import *
from ZapOnPy import ZOP
from bot import Comandos
from dados import Data



bot = ZOP(True, False)
comm = Comandos(bot)

while True:
    new_messages = bot.check_new_messages()
    if new_messages:
        if new_messages>5:
            times = int(new_messages/5)
            bot.up_to_first_message_in_chat(times)
        new_messages_list = bot.get_messages_web_elements(Msg_options.IN)

        comm.check_command(new_messages, new_messages_list)


