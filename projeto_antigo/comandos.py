import os
import pyautogui
import time
from mensagem import Message
from dados import Data

mensagem =  Message()
dado = Data()


class Commands:
    def __init__(self) -> None:
        pass
    
    def test(self, search_all_images = True):
        #clica na aba de escrever
        msg= 'Oi menó, tô por aqui!'
        mensagem.send_message_on_chat(message= msg, get_out= True, search_image= search_all_images )
        time.sleep(0.2)
        pyautogui.press('esc')

    def apresentation(self, search_all_images = True):
        local = os.getcwd()
        path = local + '/images/command_apresentation.jpg'
        texto = '''"*Yare Yare Daze... Então, você deseja adentrar no RPG de JoJo, não é? Acha que está preparado para enfrentar os desafios que este universo bizarro reserva? Prepare-se, pois aqui não é lugar para os fracos. Stands poderosos, inimigos astutos e mistérios intrigantes aguardam aqueles que ousam ingressar. Se julga capaz de lidar com a intensidade das batalhas, a imprevisibilidade dos Stands e a loucura característica deste mundo, então, caro aventureiro, desafio-o a tornar-se um Stand User. Escolha com sabedoria, planeje estrategicamente e, é claro, esteja pronto para entoar o seu melhor ORA ORA ORA quando a situação exigir. Assim, pergunto a você: aceitará o desafio de se tornar parte desta jornada bizarra? Se a resposta for afirmativa, prepare-se para uma experiência única. Boa sorte, meu camarada. Certamente, ela será necessária.* 👊🌟"'''
        mensagem.send_image_on_chat(path, texto, True, search_image= search_all_images)

    def poll(self, search_all_images = True):
        question = 'Qual é o planeta mais próximo do Sol no nosso sistema solar?'
        opcao1 = 'a) Vênus'
        opcao2 = 'b) Mercúrio'
        opcao3 = 'c) Marte'
        opcao4 = 'd) Júpiter'
        mensagem.send_poll(question, False,True,search_all_images, opcao1, opcao2, opcao3, opcao4)

    def send_DM_to(self, msg = str, search_all_images = True):
        number = msg[8:20]
        txt = msg[21:len(msg)]
        mensagem.send_direct_message(number, txt, True, search_all_images)

    def help(self, msg = str, search_all_images = True):
        '''Função Help'''
        try:
            if len(msg) == 5:
                comando = 'help'
            else:
                comando = msg[1:5] +'_'+ msg[6:len(msg)]

            with open(f'textos/{comando}.txt', 'r', encoding='utf-8') as file:
                content = file.read()
        except:
            with open(f'textos/help_error.txt', 'r', encoding= 'utf-8') as file:
                content = file.read()
        
        mensagem.send_message_on_chat(content, False, search_all_images)
        with open(f'textos/contato_dev.txt', 'r', encoding= 'utf-8') as file:
            content = file.read()
        mensagem.send_message_on_chat(content, True, search_all_images)

    def ficha(self, msg = str, search_all_images = True):
        '''Analiza os dados de uma ficha, armazena num Json e deixa na pasta chamada pendente'''
        try:
            id_p = dado.set_user_Data(msg)
            text = f'Dados da ficha armazenados com sucesso\nSeu id de player é {id_p}'
        except Exception as e:
            text = f'Ocorreu um erro, tente novamente...\n{e}\nLembre-se de sempre colocar os dados dentro dos >  <'
        mensagem.send_message_on_chat(text, True, search_all_images)

    def mostrar_dados(self, msg = str, search_all_images = True):
        try:
            id_p = msg[14:len(msg)]
            text = dado.get_user_data(id_p)
            mensagem.send_message_on_chat(text, True, search_all_images)
        except Exception as e:
            text = f'Ocorreu um erro, tente novamente...\n{e}\n Lembre-se da sintaxe do comando:\n !dados player id\n onde o id é o número'
            mensagem.send_message_on_chat(text, True, search_all_images)
        

        