from data import Data
import os

dado = Data()
text= """ Coloque sempre entre >   <
Nome: >bbbbbbb<
Descrição: >é borgwgrgrgm<
Preço: >1022200<
Quantidade: >2318<
!adicionar na loja
"""

#list = dado.set_store_itens(text, "caminho/do/arquivo")

import os

import os

def rename():
    path = './downloads'
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
    print(new_path)

rename()


