"""
Organizar todas as docStrings:


Essa classe foi feita com o intuito de facilitar o uso do ZAP ON PY, me inspirei no SELENIUM que tem uma classe
chamda By que tem as opções de procura por elementos, decidi fazer algo parecido.
"""


class msg_options:
    IN = "in"
    OUT = "out"
    ALL = "all"


class field_options:
    """Campos de inserção de texto
    """
    MESSAGE = "message"
    """Campo para escrever mensagnes
    """
    TITTLE = "tittle"
    """Campo para escrever o título em imagens e documentos
    """
    FOWARD = "foward"
    """Campo para procurar e selecionar (selecione usando send_keys(Keys.ENTER)) os contatos para encaminhar a mensagem
    """
    CONTACT = "contact"
    """Campo para procurar e entrar (entre usando send_keys(Keys.ENTER)) no chat especificado
    """
    REACTION = "reaction"
    """Campo para procurar  e selecionar uma reação no campo de reações
    """


class buttons_options:
    READMORE = "readmore"
    """Botão leia mais, clique para estender as mensagens muito longas
    """
    ATTACH = "attach"
    """Botão de anexo, clique nele para liberar o Input e para usar outras funções relacionadas
    """
    CHAT_MENU = "chat_menu"
    """Botão de menu do chat, clique para liberar as opções de menu do chat
    """
    CLEAR_CHAT = "clear_chat"
    """Boão de Limpar o chat, clique para limpar o chat (as opções de menu devem estar abertas)
    """
    CLEAR_CONFIRM = "clear_confirm"
    """Botão para confirmar a limpeza do chat, clique para limpar (opção Limpar o chat deve ter sido selecionada no menu)
    """
    FOWARD = "foward"
    """Botão para encaminhar a mensagem selecionda, clique para abrir o campo de encaminhar (Para selecionar esse botão deve primeiro
    abrir o menu da mensagem e selecionar a opcão encaminhar)
    """
    FOWARD_CONFIRM = "foward_confirm"
    """Botão para confirmar o encaminhamento de mensagens, é usado após usar o field_foward para selecionar os contatos
    para encaminhar as mensagens.
    """


class msg_menu_options:

    MSG_DATA = "Dados da mensagem"
    """Seleciona a opção DADOS DA MENSAGEM
    Deve ser usado após abrir o menu de mensagem (find_message_menu)"""
    AWSER = "Responder"
    """Seleciona a opção RESPONDER
    Deve ser usado após abrir o menu de mensagem (find_message_menu)"""
    REACT = "Reagir"
    """Seleciona a opção REAGIR
    Deve ser usado após abrir o menu de mensagem (find_message_menu)"""
    FOWARD = "Encaminhar"
    """Seleciona a opção ENCAMINHAR
    Deve ser usado após abrir o menu de mensagem (find_message_menu)"""
    FIX = "Fixar"
    """Seleciona a opção FIXAR
    Deve ser usado após abrir o menu de mensagem (find_message_menu)"""
    FAVORITE = "Favoritar"
    """Seleciona a opção FAVORITAR
    Deve ser usado após abrir o menu de mensagem (find_message_menu)"""
    DELETE = "Apagar"
    """Seleciona a opção APAGAR
    Deve ser usado após abrir o menu de mensagem (find_message_menu)"""
    EDIT = "Editar"
    """Seleciona a opção EDITAR
    Deve ser usado após abrir o menu de mensagem (find_message_menu)"""

    LIST_MENU_OPTIONS = [MSG_DATA, AWSER, REACT,
                         FOWARD, FIX, FAVORITE, DELETE, EDIT]


class reactions_options:
    pass
