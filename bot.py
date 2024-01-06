import logging
import random
import time
from dados import Data
from ZapOnPy import ZOP
from options import *
from selenium.webdriver.remote.webelement import WebElement

data = Data()

class Comandos:
    """Essa classe representa todos os comandos que poderão ser ativados pelo bot, via chat"""

    def __init__(self, ZOP_instance = object) -> None:
        self.ZOP = ZOP_instance
        self.commands_list = ["!teste", "!apresentar", "!ficha", '!aprovar player', '!dados numero']
        self.adms_numbers = ["+55 18 98800-3813", "+55 81 9605-2190"]
        

    def check_command(self, number_of_new_messages: int, messages_list: list):
        ''' Recebe uma lista de mensagens WebElements
        Checa se a mensagem entregue como parâmetro corresponde aos comandos e executa o comando
        específico'''
        time.sleep(0.5)
        try:
            for turn , message_web_element in enumerate(messages_list):
                if turn >= number_of_new_messages:
                    break
                time.sleep(0.7)
                message = self.ZOP.get_message_text(message_web_element)
                for comando in self.commands_list:
                    if comando in message:
                        self.ZOP.click_message_option(message_web_element, Msg_menu_options.REPLY)
                        break

                if "!teste" in message:
                    self.teste()
                    
                if "!apresentar" in message:
                    self.apresentar()

                if "!ficha" in message:
                    self.ficha(message)

                if '!aprovar player' in message:
                    self.aprovar(message)

                if '!dados numero' in message or '!dados número' in message:
                    self.dados_por_numero(message)

                if '!meus dados' in message:
                    self.meus_dados(message)

                if '!trocar atributos' in message:
                    self.trocar_atributos(message)

                if '!meus atributos' in message:
                    self.meus_atributos()

                if '!cena' in message:
                    self.cena(message)

                if '!ganhar pontos' in message:
                    self.colocar_pontos(message)
                
                if '!meu numero' in message:
                    self.meu_numero()
        except Exception as e:
            print(f"ERRO: {e}")

        finally:
            time.sleep(0.2)
            self.ZOP.close_chat()

    
    def teste(self):
        self.ZOP.send_message_on_chat(text= 'testando esse carambolas')

    def apresentar(self):
        text = '''"*Yare Yare Daze... Então, você deseja adentrar no RPG de JoJo, não é? Acha que está preparado para enfrentar os desafios que este universo bizarro reserva? Prepare-se, pois aqui não é lugar para os fracos. Stands poderosos, inimigos astutos e mistérios intrigantes aguardam aqueles que ousam ingressar. Se julga capaz de lidar com a intensidade das batalhas, a imprevisibilidade dos Stands e a loucura característica deste mundo, então, caro aventureiro, desafio-o a tornar-se um Stand User. Escolha com sabedoria, planeje estrategicamente e, é claro, esteja pronto para entoar o seu melhor ORA ORA ORA quando a situação exigir. Assim, pergunto a você: aceitará o desafio de se tornar parte desta jornada bizarra? Se a resposta for afirmativa, prepare-se para uma experiência única. Boa sorte, meu camarada. Certamente, ela será necessária.* "'''
        self.ZOP.send_file_in_input(Input_options.MIDIA,file_path= r"apres.jpg", tittle= text)

    def dados_player(self, message = str):
        if '!dados player' in message:
            try:
                adm = self.is_adm()
                if adm:
                    split = message.split()
                    player_id = split[2]
                    msg_to_send = data.get_user_data(player_id)
                else:
                    msg_to_send = f'Você não tem Autorização para isso!'
                    self.ZOP.send_message_on_chat(msg_to_send)
            except Exception as e:
                self.ZOP.send_message_on_chat(f"Ocorreu um erro: {e}")


    def ficha(self, message = str):
        try: #tentando achar o número de telefone.
            for i in range(5):
                number = self.ZOP.get_number()
                if number == None:
                    continue
                else:
                    break
            self.ZOP.send_message_on_chat(f"Número detectado:\nNúmero:{number}", get_out= False)
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
            
        self.ZOP.send_message_on_chat(send)

            ##procurar chat dos ademar
        
    def aprovar(self, message = str):
        try:
            number = self.ZOP.get_number()
            print(number)
            adm = self.is_adm(number)
            if adm:
                print(adm)
                split = message.split()
                player_id = split[2]
                message = data.aprove(int(player_id))
            else:
                message = f'Você não tem Autorização para isso!'
        except Exception as e:
            message = f'Ocorreu um erro:\n {e}'
        
        time.sleep(0.2)
        self.ZOP.send_message_on_chat(message)
        
    def dados_por_numero(self, message = str):
        number = message.split()[2]
        try:
            player_id = data.search_player_by_number(number)
            user_data = data.get_user_data(player_id)
        except Exception as e:
            user_data = e
        self.ZOP.send_message_on_chat(user_data)

    def meus_dados(self, message = str):
            number = self.ZOP.get_number()
            try:
                player_id = data.search_player_by_number(number)
                user_data = data.get_user_data(player_id)
            except Exception as e:
                user_data = e
            self.ZOP.send_message_on_chat(user_data)
    def trocar_atributos(self, message = str):

        number = self.ZOP.get_number()
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

        self.ZOP.send_message_on_chat(msg)
    
    def meus_atributos(self):
        number = self.ZOP.get_number()
        try:
            player_id = data.search_player_by_number(number)
            if player_id is not None:
                attributes = data.get_attributes(player_id)
                msg_to_send = attributes
            else:
                msg_to_send = f'O seu número não está no banco de dados, para se cadastrar, utilize o comando !iniciar e preencha a ficha conforme indicado.'
        except Exception as e:
            msg_to_send = e

        self.ZOP.send_message_on_chat(msg_to_send)
    
    def cena(self, message = str):

        try:
            number = self.ZOP.get_number()
            player_id = data.search_player_by_number(number)
            scene_id = data.set_scenes(player_id, message)
            response = f"Cena armazenada no player {player_id} \n id da cena: {scene_id}\nVerifique se houve alguma alteração de caractere ou palavra na sua cena\n{message}"
        except Exception as e:
            response = f"Ocorreu um erro {e}"
        self.ZOP.send_message_on_chat(response, True)
            
    def colocar_pontos(self, message):
        try:
            number = self.ZOP.get_number()
            player_id = data.search_player_by_number(number)
            points = int(message.split()[2])
            print(points, type(points))
            data.set_points(player_id, points)
            response = f"Pontos adicionados com sucesso, use !meus dados para visualizar"
        except Exception as e:
            response = f"Ocorreu um erro {e}"
        self.ZOP.send_message_on_chat(response, True)
    
    def meu_numero(self):
        try:
            number = self.ZOP.get_number()
            msg = f'Número detectado: {number}'
        except Exception as e:
            msg= f'Ocorreu um erro {e}'
            
        self.ZOP.send_message_on_chat(msg)

    

    def is_adm(self, number):
        """Checa se o número é um ADM e retorna bool"""
        if number in self.adms_numbers:
            return True
        return False
    

    def count_words(text: str):
        """conta a quantidade de palavras

        Args:
            text (str): o texto em string

        Returns:
            int : quantidade de palavras do texto
        """
        number_of_words = 0
        list =  text.split()
        for word in list:
            for index, letter in enumerate(word):
                if letter.isalpha() or letter in ["!", ".", ",", "?", ")", "%", "-"]:
                    if index == len(word) -1:
                        number_of_words +=1
        return number_of_words
                
    
    
    def calcular_acerto(precisao_personagem, precisao_distancia):
        """Calcula o acerto de um projétil com base na precisão do personagem e na precisão baseada na distância.

        Args:
            precisao_personagem: A precisão do personagem, em porcentagem.
            precisao_distancia: A precisão baseada na distância, em porcentagem.

        Returns:
            Uma porcentagem que representa a probabilidade de acerto do projétil.
            Também retorna as chances de todos os 10 tiros errarem.
        """

        if precisao_distancia < 0 or precisao_distancia > 100:
            raise ValueError("A precisão baseada na distância deve estar entre 0 e 100.")

        taxa_acerto = (precisao_personagem + precisao_distancia) / 2
        chances_de_erro = 100 - taxa_acerto

        # Arredonda a taxa de acerto e as chances de erro para o inteiro mais próximo.

        tiros_acertados = 0
        tiros_errados = 0
        for _ in range(10):
            if random.randint(0, 100) <= taxa_acerto:
                tiros_acertados += 1
            else:
                tiros_errados += 1
        probabilidade_errar_tudo = (chances_de_erro / 100) ** 10
        return taxa_acerto, chances_de_erro, tiros_acertados, tiros_errados, probabilidade_errar_tudo

    



        

