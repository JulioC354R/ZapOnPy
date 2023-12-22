import logging
import time
from dados import Data
from ZapOnPy import ZOP
from BotRPG import Bot
rpg = Bot()
data = Data()

class Comandos:
    """Essa classe representa todos os comandos que poderão ser ativados pelo bot, via chat"""

    def __init__(self, bot_instance = object) -> None:
        self.bot = bot_instance
        self.commands_list = []
        

    def check_command(self, message):
        '''Checa se a mensagem entregue como parâmetro corresponde aos comandos e executa o comando
        específico'''
        time.sleep(0.5)
        if '!teste' in message:
            self.bot.send_message_on_chat(text= 'testando esse carambolas')
        
        if '!apresentar' in message:
            text = '''"*Yare Yare Daze... Então, você deseja adentrar no RPG de JoJo, não é? Acha que está preparado para enfrentar os desafios que este universo bizarro reserva? Prepare-se, pois aqui não é lugar para os fracos. Stands poderosos, inimigos astutos e mistérios intrigantes aguardam aqueles que ousam ingressar. Se julga capaz de lidar com a intensidade das batalhas, a imprevisibilidade dos Stands e a loucura característica deste mundo, então, caro aventureiro, desafio-o a tornar-se um Stand User. Escolha com sabedoria, planeje estrategicamente e, é claro, esteja pronto para entoar o seu melhor ORA ORA ORA quando a situação exigir. Assim, pergunto a você: aceitará o desafio de se tornar parte desta jornada bizarra? Se a resposta for afirmativa, prepare-se para uma experiência única. Boa sorte, meu camarada. Certamente, ela será necessária.* "'''
            self.bot.send_midia(r"apres.jpg", text)
        
        # consertar
        if '!dados player' in message:
            try:
                adm = self.bot.is_adm()
                if adm:
                    split = message.split()
                    player_id = split[2]
                    msg_to_send = data.get_user_data(player_id)
                else:
                    msg_to_send = f'Você não tem Autorização para isso!'
                    self.bot.send_message_on_chat(msg_to_send)
            except Exception as e:
                self.bot.send_message_on_chat(f"Ocorreu um erro: {e}")
        
        if '!ficha' in message:
            try: #tentando achar o número de telefone.
                for i in range(5):
                    number = self.bot.get_number()
                    if number == None:
                        continue
                    else:
                        break
                self.bot.send_message_on_chat(f"Número detectado:\nNúmero:{number}", get_out= False)
                logging.info('Comando !ficha encontrado')
                user = data.extract_data(message)
                found = data.search_player_by_number(number)
                if found == None:
                    id_p = data.set_user_data(user, number = number)
                    send = f'''Sua ficha está aguardando uma aprovação dos nossos ADMs, por gentileza aguarde ou solicite a algum ADM a verificação. \nId do player: {id_p} \nStatus: pendente'''
                else:
                    send = f'Seu número já está cadastrado, utilize o comando\n *!meus dados* para obter os dados'
            except Exception as e:
                send = f'ocorreu um erro, por favor reportar ao adm:\n{e}'
                
            self.bot.send_message_on_chat(send)

            ##procurar chat dos ademar
        
        
        if '!aprovar player' in message:
            try:
                number = self.bot.get_number()
                adm = rpg.is_adm(number)
                if adm:
                    split = message.split()
                    player_id = split[2]
                    message = data.aprove(int(player_id))
                else:
                    message = f'Você não tem Autorização para isso!'
            except Exception as e:
                message = f'Ocorreu um erro:\n {e}'
            self.bot.send_message_on_chat(message)
        
        
        if '!dados numero' in message or '!dados número' in message:
            number = message.split()[2]
            try:
                player_id = data.search_player_by_number(number)
                user_data = data.get_user_data(player_id)
            except Exception as e:
                user_data = e
            self.bot.send_message_on_chat(user_data)

        if '!meus dados' in message:
            number = self.bot.get_number()
            try:
                player_id = data.search_player_by_number(number)
                user_data = data.get_user_data(player_id)
            except Exception as e:
                user_data = e
            self.bot.send_message_on_chat(user_data)

        if '!trocar atributos' in message:
            number = self.bot.get_number()
            print(number)
            #try:
            player_id = data.search_player_by_number(number)
            print(player_id)
            attributes_list = data.extract_data(message)
            for index, attrib in enumerate(attributes_list):
                attributes_list[index] = int(attrib)

            sucess = data.set_attributes(player_id,attributes_list)
            print(sucess)
            if sucess:
                msg = f'Atributos atualizados'
            else: 
                msg = f'Não foi possível atualizar os atributos!'
            #except Exception as e:
                #msg = f'Fahou: {e}'

            self.bot.send_message_on_chat(msg)

        if '!meus atributos' in message:
            number = self.bot.get_number()
            try:
                player_id = data.search_player_by_number(number)
                if player_id is not None:
                    attributes = data.get_attributes(player_id)
                    msg_to_send = attributes
                else:
                    msg_to_send = f'O seu número não está no banco de dados, para se cadastrar, utilize o comando !iniciar e preencha a ficha conforme indicado.'
            except Exception as e:
                msg_to_send = e

            self.bot.send_message_on_chat(msg_to_send)

        if '!cena' in message:
            try:
                number = self.bot.get_number()
                player_id = data.search_player_by_number(number)
                scene_id = data.set_scenes(player_id, message)
                response = f"Cena armazenada no player {player_id} \n id da cena: {scene_id}\nVerifique se houve alguma alteração de caractere ou palavra na sua cena\n{message}"
            except Exception as e:
                response = f"Ocorreu um erro {e}"
            self.bot.send_message_on_chat(response, True)
            
        if '!ganhar pontos' in message:
            try:
                number = self.bot.get_number()
                player_id = data.search_player_by_number(number)
                points = int(message.split()[2])
                print(points, type(points))
                data.set_points(player_id, points)
                response = f"Pontos adicionados com sucesso, use !meus dados para visualizar"
            except Exception as e:
                response = f"Ocorreu um erro {e}"
            self.bot.send_message_on_chat(response, True)
            
        if '!meu numero' in message:
            try:
                number = self.bot.get_number()
                msg = f'Número detectado: {number}'
            except Exception as e:
                msg= f'Ocorreu um erro {e}'
                
            self.bot.send_message_on_chat(msg)
                


        

