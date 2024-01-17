import json
import os


class Data:
    """Esta classe é responsável por gerenciar os dados do RPG e do bot.
    """

    def check_player_status(self, player_id: int):
        """Checa se o player foi aprovado pelos ADMs

        Args:
            player_id (int): _description_

        Returns:
            Bool : O boolean dizendo se ele foi aprovado ou não.
        """
        status = self.get_player_dict(player_id)["status"]
        if status == "approved":
            return True
        else:
            return False


    def aprove(self, player_id):
        '''altera o status do player para approved. retorna info, uma string em forma de mensagem para informar se o processo foi bem sucedido ou não.
        Parâmetros:
        \nplayer_id = int -> o id do player'''

        try:
            user = self.get_player_dict(player_id)
            user["status"] = "approved"
            self.update_player_data(player_id= player_id, user_data= user)
            info = f'O player {player_id} foi aprovado!'
        except Exception as e:
            info = f'Não foi possível realizar essa operação: {e}'

        return info

    def extract_data(self, text=str):
        '''Essa função lê a ficha de usuário recebida, extrai os dados e retorna numa lista.
        \nParâmetros:
        \ntext = str -> texto, formulário (ficha) do usuário.'''

        # pega os indices de onde começa e onde termina cada dado dos personagens
        indices_init = [i for i, char in enumerate(text) if char == '>']
        indices_final = [i for i, char in enumerate(text) if char == '<']

        # list compregention, pega os valores que estão entre > <
        values_user = [text[indices_init[index]+1:indices_final[index]]
                       for index in range(len(indices_init))]
        # tira o primeiro dado que é inútil já que na ficha tem um >< para exemplificar
        if values_user[0].split() == []:
            values_user.pop(0)
        final_list = []

        # aqui estou tirando quebras de linhas e depois adicionando espaços a cada palavra
        for values in values_user:
            value = values.replace('\n', '').split()
            value = ' '.join(value)
            final_list.append(value)

        return final_list

    def set_user_data(self, extracted_user_data=list, player_id=0, status = "pending", total_points=300, wallet=2000, number=''):
        '''Essa função sobreescreve ou cria o json com dados do novo usuário. 
        \nParâmetros:
        \nplayer_id = 0 | int -> é o id do player, se não for definido ao chamar é 0
        \ntotal_points = 300 | int é o total de pontos a ser distribuído
        \nwallet = 2000 | int '''

        if player_id == 0:
            player_id = self.get_new_player_id()

        user_keys = ["name", "age", "appearance", "personality", "history",
                     "sexuality", "gender", "height", "weight", "organization",
                     "stand_name", "stand_type", "stand_powers"]
        dict_user = dict(zip(user_keys, extracted_user_data))

        attributes_keys = ["strength", "resistance", "speed", "precision",
                           "stand_strength", "stand_resistance", "stand_speed", "stand_precision"]
        attributes_values = [0 for i in range(8)]

        dict_attributes = dict(zip(attributes_keys, attributes_values))

        new_user = {"user": {"player_id": player_id, "status": status, **dict_user, "wallet": wallet, "total_points": total_points, "stand_total_points": total_points,
                             "attributes": {**dict_attributes}, "inventary": {}, "phone_number": number, "scenes": {}}}

        with open('RPG/players.json', 'r', encoding='utf-8') as file:
            try:
                players_data = json.load(file)
                # Verificar se a chave "data" está presente no dicionário carregado
                if "data" in players_data:
                    users = players_data["data"]
                else:
                    users = []
            except json.JSONDecodeError:
                users = []

        # Adicionar o novo usuário à lista
        users.append(new_user)

        data = {"data": users}

        self.write_json(data, 'RPG/players.json')
        return player_id

    def set_attributes(self, player_id=int, points=list):
        '''Lê o Json, pega o usuário que tem o ID correspondente e substitui os valores dos atributos
        usando os dados da lista points, retorna um bool informando o sucesso da operação.
        \nParâmetros:
        \nplayer_id = int -> é o ID do jogador.
        \npoints = list -> lista de pontos a serem distribuídos.
        '''
        # bool para aprovar a troca de atributos.
        user = self.get_player_dict(player_id)

        # pegando os valores do Json e definindo variáveis
        total_points = user["user"]["total_points"]
        stand_total_points = user["user"]["stand_total_points"]
        attributes = user["user"]["attributes"]

        # aqui estou criando uma lista com as chaves dos atributos
        keys = list(attributes.keys())
        # vou definir como valor de cada atributo o points de index correspondente.
        for index, key in enumerate(keys):
            attributes[key] = points[index]
        # se a soma dos pontos ultrapassar os pontos totais do personagem ou stand, não escreva os dados.
        if sum(points[0:4]) > total_points or sum(points[4:8]) > stand_total_points:
            approve = False

        # se aprovado, escreva os dados.
        if approve:
            self.update_player_data(player_id= player_id, user_data= user)

        return approve

    def get_user_data(self, id_player):
        '''Essa função os dados do usuário, extrai os dados e retorna uma string personalizada. 
        \nParâmetros:
        \nid_player = str -> Id do player'''

        try:
            user = self.get_player_dict(id_player)

            # lista de chaves em pt_br para usar
            keys_pt_br = ["Player_ID", "Status", "Nome", "Idade", "Aparência", "Personalidade", "História", "Sexualidade", "Gênero", "Altura", "Peso", "Organização",
                          "Nome do Stand", "Tipo de Stand", "Habilidades do Stand", "Carteira",  "Pontos Personagem", "Pontos Stand", "Atributos", "Inventário", "Contato"]
            # usando list comprehention para pegar os valores
            values = [value for key, value in user.items()]

            # substitui o dicionário de atributos pela string dos atributos pegos na função.
            values[-4] = self.get_attributes(id_player)

            # segue como uma string no formato f'{key_pt_br}: {value}'
            # o join vai pular uma linha a cada string dessa lista
            string_data = "\n".join(
                [f'{key}: {value}' for key, value in zip(keys_pt_br, values)])
            return string_data
        except Exception as e:
            return e

    def write_json(self, dict=dict, path=str):
        with open(path, 'w', encoding= "utf-8") as arquivo_saida:
            json.dump(dict, arquivo_saida, indent=4)

    def get_new_player_id(self):
        '''Pega um o ultimo id de player +1, sendo assim, teremos um novo id de player, retorna esse novo id'''

        with open(f'RPG/players.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        ids_list = []
        users = data["data"]
        for user in users:
            id_p = user["user"]["player_id"]
            ids_list.append(id_p)

        for new_id in range(9999):
            if new_id not in ids_list:
                new_player_id = new_id
                break

        return new_player_id

    def search_player_by_number(self, number=str):
        '''procura o player pelo número e retorna o id do player, se não encontrar retorna None'''
        with open(f'RPG/players.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        users = data["data"]
        for user in users:
            phone_number = user["user"]["phone_number"]
            if phone_number == number:
                return user["user"]["player_id"]

        return None

    # falta terminar

    def set_number(self, number=str):
        with open(f'RPG/players.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        users = data["data"]
        for user in users:
            phone_number = user["user"]["phone_number"]
            phone_number = number

    def get_attributes(self, player_id):

        user = self.get_player_dict(player_id)
        attributes = user["attributes"]

        key_pt_br = ["\n*Força      *", "*Resistência*", "*Velocidade *", "*Precisão   *",
                     "*Força do Stand      *", "*Resistência do Stand*", "*Velocidade do Stand *", "*Precisão do Stand   *"]
        # usando list comprehention para pegar os valores
        values = [value for key, value in attributes.items()]

        converted = []  # lista dos dados convertidos em str

        converted.append(
            str(values[0]) + f'*    conversão: ' + str(int(values[0] / 100 * 20)) + ' kg*')
        converted.append(
            str(values[1]) + f'*    conversão: ' + str(int(values[1] / 100 * 20)) + ' kg*')
        converted.append(
            str(values[2]) + f'*    conversão: ' + str(int(values[2] / 100 * 10)) + ' m/s*')
        converted.append(
            str(values[3]) + f'*    conversão: ' + str(int(values[3] / 150 * 10)) + ' %*')
        converted.append(
            str(values[4]) + f'*    conversão: ' + str(int(values[4] / 100 * 20)) + ' kg*')
        converted.append(
            str(values[5]) + f'*    conversão: ' + str(int(values[5] / 100 * 20)) + ' kg*')
        converted.append(
            str(values[6]) + f'*    conversão: ' + str(int(values[6] / 100 * 10)) + ' m/s*')
        converted.append(
            str(values[7]) + f'*    conversão: ' + str(int(values[7] / 150 * 10)) + ' %*')

        # segue como uma string no formato f'{key_pt_br}: {value}'
        # o join vai pular uma linha a cada string dessa lista
        string_data = "\n".join(
            [f'{key}: {value}' for key, value in zip(key_pt_br, converted)])
        return string_data

    def set_scenes(self, player_id=int, scene=str):
        user = self.get_player_dict(player_id)
        scenes = user["scenes"]

        for i in range(9999):
            scene_id = str(i)
            if scene_id not in scenes:
                print("Novo ID de cena:", i)
                break

        user["scenes"] = {**scenes, scene_id: scene}
        self.update_player_data(player_id, user)
        return scene_id

    def get_scene(self, player_id=int, scene_id=int):
        user = self.get_player_dict(player_id)
        scenes = user["scenes"]
        scene = scenes[str(scene_id)]

        return scene

    def get_player_dict(self, player_id):
        with open('RPG/players.json', 'r', encoding='utf-8') as file:
            players_data = json.load(file)
            users = players_data["data"]
            player_found = {}

            for user in users:
                if user["user"]["player_id"] == player_id:
                    player_found = user["user"]
                    break
            return player_found

    def update_player_data(self, player_id=int, user_data=dict):
        with open('RPG/players.json', 'r', encoding='utf-8') as file:
            players_data = json.load(file)
            users = players_data["data"]

            for user in users:
                if user["user"]["player_id"] == player_id:
                    user["user"] = user_data
                    break

        self.write_json(players_data, 'RPG/players.json')

    def set_points(self, player_id=int, points_to_add=int):
        user = self.get_player_dict(player_id)
        user["total_points"] += points_to_add
        user["stand_total_points"] += points_to_add
        self.update_player_data(player_id, user)

    
    def get_store_items(self, all = True, item_id = 0) -> (list|dict):
        """ Retorna uma lista de dicionários que são os itens da loja ou o dicionário com o id de item correspondente."""
        with open("RPG/store.json", "r", encoding= "utf8") as file:
            store = json.load(file)
            store_items = store["data"]["items"]
            if all:
                return store_items
            for item in store_items:
                if item["id"] == item_id:
                    return item


    def set_store_itens(self, text: str, image_path: str):

        ids_list = []

        list_values = self.extract_data(text)
        items = self.get_store_items(True)

        for item in items:
            ids_list.append(item["id"])
        
        for new_id in range(9999):
            if new_id not in ids_list:
                break
        
        list_values = [new_id, *list_values, image_path]
        list_keys = ["id", "name", "description", "price", "stock_quantity", "image"]
        new_item_dict = dict(zip(list_keys, list_values))
        items = [*items, new_item_dict]
        items_json_format = {"data": {"items": [*items]}}
        self.write_json(dict=items_json_format, path= "./RPG/store.json")
        print(items_json_format)
    
    def rename_downloads(self, path = './downloads'):
        """Renomeia os downloads feitos no whatsapp, fazendo com que os nomes sejam estáticos e mais fáceis de manipular 
        as mídias que o bot baixou"""
        files = os.listdir(path)

        # pega os arquivos que foram baixados diretamente do whatsapp.
        whatsapp_files = [file for file in files if "WhatsApp" in file]

        # renomeia os arquivos adicionando um número a eles
        for i, file in enumerate(whatsapp_files, start=1):
            new_name = f"Media_{i}{os.path.splitext(file)[1]}"
            new_path = os.path.join(path, new_name)

            # Check if the new name already exists and increment the number until finding a unique name
            while os.path.exists(new_path):
                i += 1
                new_name = f"Media_{i}{os.path.splitext(file)[1]}"
                new_path = os.path.join(path, new_name)

            original_path = os.path.join(path, file)
            os.rename(original_path, new_path)
            print(f"Arquivo Renomeado: {original_path} -> {new_path}")
        return new_path
            
        
