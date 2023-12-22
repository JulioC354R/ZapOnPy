import json
import os
import logging


class Data:
    def __init__(self) -> None:
        pass
    
    def is_approved(self, p_id):
        '''Essa função verifica se o json do player está na pasta de player, e retorna o bool'''
        json_path = f'RPG/players/player{p_id}.json'
        approved = os.path.exists(json_path)
        return approved

    def is_pending(self, p_id):
        '''Essa função verifica se o json do player está na pasta de pendente, e retorna o bool'''
        json_path = f'RPG/pendente/pendente{p_id}.json'
        pending = os.path.exists(json_path)
        return pending

    
    def set_user_Data(self, form= str):
        '''Essa função lê a ficha recebida e extrai os dados para escrever
        num Json contendo os dados do usuário'''
        #pega os indices de onde começa e onde termina cada dado dos personagens
        indices_init  = [i for i, char in enumerate(form) if char == '>']
        indices_final = [i for i, char in enumerate(form) if char == '<']

        #list compregention, pega os valores que estão entre > < 
        values_user = [form[indices_init[index]+1:indices_final[index]] for index in range(len(indices_init))]
        #tira o primeiro dado que é inútil já que na ficha tem um >< para exemplificar
        values_user.pop(0)

        #lista de chaves para os dados,
        keys_user = ["name", "age", "appearance", "personality", 
                     "history", "sexuality", "gender", "height", "weight", "organization", 
                     "money", "inventory", "physical_strength", "general_resistance", 
                     "speed/agility", "aim/precision", "total_points"]

        # Índices que precisam ser convertidos para int
        indices_int = [12, 13, 14, 15]

        # Converte valores para inteiros
        for index, values in enumerate(values_user):
            if index in indices_int:
                #aqui o join tá juntando os itens da lista, esses itens são
                #qualquer char dentro de valores se ele for um digito.
                num = ''.join([char for char in values if char.isdigit()])
                values_user[index] = int(num)
        
        #adiciona ao último valor o total de pontos atribuídos
        values_user.append(sum(values_user[12:16]))
 
        #usa dict e zip para juntar as duas listas e transformar em dict
        user = dict(zip(keys_user,values_user))
        logging.info(f'Dicionário criado: {user}')
        #criando o id do player e procurando se ele já existe(o Json com esse nome)

        for id_player in range(999):
            approved = self.is_approved(id_player)
            if approved:
                status = 'approved'
                path = f'RPG/players/player{id_player}.json'
                break

        #se esse id ainda não foi aprovado, coloca os dados em pendente.
        if not approved:
            for id_pending in range(999):
                pending = self.is_pending(id_pending)
                if pending:
                    status = 'pending'
                    path = f'RPG/pendente/pendente{id_player}.json'
                    break
            
        i=0
        #adicionando id de jogador no começo do dict e o status dele
        user = {"player_id": id_player, "status": status **user}

        with open (path,'w+', encoding= 'utf-8') as file:
            file.writelines('{\n    "data": [\n        {\n            "user": {\n')
            for key, value in user.items():
                #is isntance verifica se o valor de vez é str
                if isinstance(value, str):
                    #tira as quebras de linhas \n e \r
                    value = value.replace('\n', '').replace('\r', '')
                if i < len(user) -1:
                    file.writelines(f'                "{key}": "{value}", \n')
                else:
                    file.writelines(f'                "{key}": "{value}"\n')
                i+=1
            file.writelines('            }\n        }\n    ]\n}')
        return id_player

    def get_user_data(self, id_p):
        '''Retorna o valor num formato de string para mostrar ao player'''
        with open(f'RPG/player{id_p}.json', 'r', encoding='utf-8') as file:
            data = json.loads(file.read())
            user = data['data'][0]['user']
            #aqui eu usei um join que vai adicionar uma quebra de linha a cada item
            #cada item é pertencente a uma lista feita com o list comprehention onde
            key_pt_br = ["Player_ID", "Nome", "Idade", "Aparência", "Personalidade", 
                         "História", "Sexualidade", "Gênero", "Altura", "Peso", 
                         "Organização", "Carteira", "Inventário", "Força_Física", 
                         "Resistência_Geral", "Velocidade/Agilidade", "Pontaria/Precisão", 
                         "Total_de_Pontos"]
            #usando list comprehention para pegar os valores
            values = [value for key, value in user.items()]

            #adicionando fator de conversão ao lado dos dados: 13.14.15.16
            #força
            values[13] = values[13] + f' conversão: {int(int(values[13]) /100 *20)} kg'
            #resistência
            values[14] = values[14] + f' conversão: {int(int(values[14]) /100* 20)} kg'
            #velocidade
            values[15] = values[15] + f' conversão: {int(int(values[15]) /100* 10)} m/s'
            #precisão
            values[16] = values[16] + f' conversão: {int(int(values[16]) /150* 10)} %'

            #segue como uma string no formato f'{key_pt_br}: {value}'
            #o join vai pular uma linha a cada string dessa lista
            string_data = '\n'.join([f'{key}: {value}' for key, value in zip(key_pt_br,values)])
            
            return string_data