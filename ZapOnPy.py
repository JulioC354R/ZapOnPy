import os
import re
import time
import logging
import pyperclip
from qr import QR
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
from selenium.webdriver.common.keys import Keys
from options import *
import pyvirtualdisplay
#
# APRENDER SOBRE DECORATORS E USAR ESSA FUNÇÃO PARA DAR LOG AO EXECUTAR CADA UMA DAS MINHAS FUNÇÕES.
#
#
# #

""" 
def log_execution(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Executando função: {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Função {func.__name__} concluída")
        return result
    return wrapper


"""


class ZOP:
    """Essa classe é responsável pelas interações diretas do selenium com o whatsapp-web, inclui funções de interação com mensagens, fazer o login, pegar números e etc."""

    def __init__(self, save_login: bool, headless: bool) -> None:
        # Desativa logging do Selenium
        logging.getLogger('selenium').propagate = False
        self.action = None
        self.browser = None
        self.approved = False
        self.virtual_display = pyvirtualdisplay.Display(
            visible=False, size=(640, 480))
        self.login(save_login, headless)

    def login(self, save_login, headless):
        qrcode_xpath = '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas'
        '''Inicializar o webdriver com os dados de login ou não'''
        driver_path = "./driver/chromedriver"    # no windows colocar chromedriver.exe
        service = webdriver.ChromeService(executable_path=driver_path)

        if save_login or headless:
            options = webdriver.ChromeOptions()
            # ao usar linux alterar para 'chromewithlogin/'
            userdir = os.path.abspath('chromewithlogin/')
            if save_login:
                options.add_argument(f"--user-data-dir={userdir}")
            if headless:
                # Executar em modo headless
                options.add_argument('--headless=new')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1200x600')
            self.browser = webdriver.Chrome(options=options, service=service)
        else:
            # iniciar sem nenhuma configuração
            self.browser = webdriver.Chrome(service=service)
        # inicializando action Chains
        self.action = ActionChains(self.browser)

        self.browser.get('https://web.whatsapp.com/')

        self.qrcode_in_terminal(qrcode_xpath)

        time.sleep(5)

        wait_time = 20
        try:
            WebDriverWait(self.browser, wait_time).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, '_3WByx'))
            )
            logging.info('Whatsapp aberto, sucesso no login.')
            self.approved = True
        except Exception as e:
            logging.error(f"Erro ao abrir o Whatsapp \n{e}")

    def qrcode_in_terminal(self, qrcode_xpath):
        for _ in range(5):
            try:
                qrcode = WebDriverWait(self.browser, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, qrcode_xpath))
                )
                qrcode.screenshot('qrcode.png')
                qr = QR()
                qr.read_qrcode_img('qrcode.png')
                time.sleep(10)
            except (NoSuchElementException, TimeoutException):
                logging.info("Qr code não encontrado.")
                break

    def close_browser(self):
        if self.browser is not None:
            self.browser.quit()
            self.browser = None

    def check_new_messages(self):
        """Pode ser usado a qualquer momento.
        Abre automaticamente o chat que contem novas mensagens

        Returns:
            int : O número de novas mensagens no elemento do icone de novas mensagens

        Utilização:
            Use a função self.get_messages() passando a quantidade de novas mensagens multiplicado
            por -1 como index, assim vai pegar somente as novas mensagens daquele chat

            OBS: ele encontra vários elementos mas a função [last()] no fim do xpath só retorna o ultimo
        """

        new_messages_xpath = "//div[@class='_2H6nH']//span[@aria-label='Não lidas'][last()]"
        try:
            WebDriverWait(self.browser, 300).until(
                EC.visibility_of_element_located((By.XPATH, new_messages_xpath)))

            new_messages_element = self.browser.find_element(
                By.XPATH, new_messages_xpath)

            number_of_new_messages = int(new_messages_element.text)
            self.browser.find_element(
                By.XPATH, '//*[@id="pane-side"]//div[contains(@class, "_2H6nH")][last()]').click()

            logging.info(
                f"Foram encontradas novas mensagens: {number_of_new_messages}")
            return number_of_new_messages
        except (NoSuchElementException, TimeoutException):
            logging.info("Não foram encontradas novas mensagens")
            return 0

    def get_messages(self, option=Msg_options.ALL):
        """Retorna uma lista de mensagens em string

        Args:
            option (str, optional): Opção de mensagem, pode ser In, Out ou All. Defaults to ALL.

        :Usage:
            ::

                #Exemplo para pegar todos os tipos de mensagem:
                messages = get_messages(option = Msg_options.ALL)

        Returns:
            _type_: _description_
        """
        elements_message = self.find_messages(option)
        messages = []

        for message in elements_message:
            print(f'texto: {message.text}')
            messages.append(message.text)
        return messages

    def get_last_message(self, option: str):
        '''Pega a última mensagem em str e retorna ela, caso der erro, retorna None'''
        # Localiza todos os botões "Leia mais"

        try:
            self.click_on_readmore()
            time.sleep(0.5)
            last_message = self.get_messages(option)[-1]
            logging.info(f'Mensagem pega: {last_message}')
            return last_message
        except NoSuchElementException:
            pass
        except Exception as e:
            logging.error(f"Erro ao obter última mensagem: {e}")
            return None

    def up_to_first_message_in_chat(self, scale=10):
        """Sobe até a a primeira mensagem do chat utilizando o botão HOME para carregar mais mensagens.
        Também executa a função readmore

        Args:
            scale (int, optional): É a quantidade de teclas HOME que vai simular. Defaults to 10.

        """
        try:

            # Apertar home para subir a página e carregar mais mensagens
            chat = self.find_chat()
            for _ in range(scale):
                chat.send_keys(Keys.HOME)
                time.sleep(0.2)

            self.click_on_readmore()
            logging.info(f'Função executada:')

        except Exception as e:
            logging.error(f"Erro ao obter todas as mensagens: {str(e)}")

    def send_message_on_chat(self, text: str, get_out=True):
        '''Envia uma mensagem quando o chat tá aberto, o get_out é para sair do chat ao enviar a mensagem'''
        self.false_typing(1.5)
        time.sleep(0.5)
        try:
            self.virtual_display.start()
            pyperclip.copy(text)
            time.sleep(0.5)
            message_field = self.find_field(Field_options.MESSAGE)
            message_field.send_keys(Keys.CONTROL, "v")
            time.sleep(0.2)
            # edit = self.browser.find_element(
            # By.XPATH, '//div[@class="_3Uu1_"]//div[@class="g0rxnol2 ln8gz9je lexical-rich-text-input"]//div[@class="to2l77zo gfz4du6o ag5g9lrv bze30y65 kao4egtt"]//span[@class="selectable-text copyable-text"]')

            message_field.send_keys(".")
            message_field.send_keys(Keys.BACK_SPACE)
            time.sleep(0.5)
            # Pressiona "Enter" para enviar a mensagem
            message_field.send_keys(Keys.ENTER)
            logging.info('Mensagem enviada')
            self.virtual_display.stop()
        except Exception as e:
            logging.error(f'Ocorreu um erro ao mandar a mensagem {e}')
        if get_out:
            self.close_chat()

    #
    # Fazer false_typing pegar um tempo aleatório a enviar, para que não seja reconhecido como bot.
    # #
    def false_typing(self, wait_seconds: float):
        '''Finge estar digitando pelo tempo de espera passado.
        Parâmetros:
        \nwait_seconds = float -> tempo de espera'''
        try:
            logging.info(f'Fingindo digitação por {wait_seconds} segundos.')
            message_field = self.find_field(Field_options.MESSAGE)
            message_field.send_keys('-')
            time.sleep(wait_seconds)
            message_field.send_keys(Keys.BACKSPACE)
        except Exception as e:
            logging.error(f'Ocorreu um erro: {e}')

    def send_file_in_input(self, option: int, file_path: str, tittle=""):
        """Envia o arquivo ao input especificado, inclui o click no attach icon.

        Args:
            file_path (str): Caminho do arquivo a ser enviado nos inputs. Defaults to str.
            tittle (str): String a ser colocada no título da mídia. Defaults to " ".

        Usage:
            ::

                from options import *
                zop.send_file_in_input(Input_options.DOCUMENT)

        """
        self.find_button(Buttons_options.ATTACH).click()
        # obtendo o caminho real do arquivo
        file_path = os.path.abspath(file_path)
        pyperclip.copy(tittle)
        files_input = self.browser.find_elements(
            By.CSS_SELECTOR, "input[type='file']")
        files_input[option].send_keys(file_path)  # enviando arquivo pelo input
        time.sleep(0.5)
        # apenas procurar o título nessas duas condições
        if option == Input_options.DOCUMENT or Input_options.MIDIA:
            tittle_field = self.find_field(Field_options.TITTLE)
            tittle_field.send_keys(Keys.CONTROL, "v")
            time.sleep(0.5)
            tittle_field.send_keys(Keys.ENTER)

        list_options = ["DOCUMENT", "MIDIA", "STICKER"]
        logging.info(
            f"Documento enviado como {list_options[option]}: {file_path}")

    def search_contact(self, contact: str):
        '''procura o contato e entra na conversa'''
        try:
            contact_field = self.find_field(Field_options.CONTACT)
            contact_field.send_keys(contact, Keys.ENTER)
            time.sleep(0.2)
            contact_field.send_keys(Keys.CONTROL, "a")
            contact_field.send_keys(Keys.BACKSPACE)
        except Exception as e:
            logging.error(f'Ocorreu um erro: {e}')

    def click_on_readmore(self):
        '''Função que clica em todos os "leia mais", para que as mensagens fiquem completas'''
        readmore_bottons = self.find_button(Buttons_options.READMORE)
        for botton in readmore_bottons:
            botton.click()

    def close_chat(self):
        try:
            time.sleep(0.2)
            self.find_field(Field_options.MESSAGE).send_keys(Keys.ESCAPE)
            logging.info('Fechando o chat')
        except:
            logging.info(f'Não conseguiu fechar o chat')

    # atualizar o get Number, LEMBRAR QUE SEMPRE AO PROCURAR UM ELEMENTO QUE NÃO APARECE SEMPRE NA TELA, UTILIZAR O MOVE-TO
    # para mover até o elemento e assim ele ficar visível.
    def get_number(self, return_chat_type=False):
        '''Pega o número da ultima mensagem do chat/grupo que está aberto por meio dos xpaths'''
        time.sleep(0.25)
        chat_type = ''
        try:
            try:
                # pega todos os elementos (aquele nome em do contato que fica na mensagem no grupo)
                # no whatsapp pt-br ele fica com esse texto dentro do elemento da classe _3B19s, acredito que dê pra adaptar pra inglês também
                xpath_numero = "//div[@class='_3B19s']//*[contains(@aria-label, 'Abrir os dados da conversa com')]"
                elements = self.browser.find_elements(By.XPATH, xpath_numero)
                if elements == []:
                    elements = self.browser.find_elements(
                        By.CLASS_NAME, "WJuYU")
                # clica no último, sendo assim, clica no elemento da ultima mensagem.
                last = elements[-1]
                last.click()
                time.sleep(0.5)
                chat_type = "group"

            except:
                # xpath da caixa de contato, a que fica em cima do chat e tem os detalhes do contato
                details = self.browser.find_element(By.CLASS_NAME, '_2au8k')
                details.click()
                time.sleep(0.5)
                chat_type = "private"
                # Inicializa uma lista de XPath a serem tentados em ordem, esses Xpaths são onde tem o número de telefone
                # os xpaths são diferentes pois no whatsapp ele difere de contato salvo, não salvo e comercial assim os números ficam em lugares diferentes

            xpath_list = [
                '//span[@class="_11JPr selectable-text copyable-text"]//span[@class="enbbiyaj e1gr2w1z hp667wtd"]',
                '//div[@class="Mk0Bp _30scZ"]/span[@class="l7jjieqr cw3vfol9 _11JPr selectable-text copyable-text"]',
                '//span[@class="_11JPr selectable-text copyable-text"]//span[@class="fe5nidar fs7pz031 tl2vja3b e1gr2w1z"]']
            # Inicializa uma lista para armazenar os números de telefone encontrados
            numeros_de_telefone = []

            # Itera sobre os XPath
            for xpath_numero in xpath_list:
                try:
                    # se achar nesses xpath um texto que tenha a formatação de um número de telefone (atualmente só funcionou pra números PT-BR)
                    # ele vai colocar dentro da lista e se achar algum ele para  o loop

                    elemento_numero = self.browser.find_element(
                        By.XPATH, xpath_numero)
                    texto_numero = elemento_numero.text
                    # Define a expressão regular para extrair números de telefone
                    padrao_telefone = re.compile(
                        r'\+\d{2} \d{2} \d{4,5}-\d{4}')
                    # Encontra números de telefone usando a expressão regular
                    numeros_de_telefone = padrao_telefone.findall(texto_numero)
                    # Se encontrou o número, sai do loop
                    if numeros_de_telefone:
                        break

                except:
                    # Se não encontrou o elemento, continua para o próximo XPath
                    continue

            # números de telefone encontrados
            number = numeros_de_telefone[0]

            xpath_botao_fechar = self.browser.find_element(
                By.XPATH, '//div[@role="button" and @aria-label="Fechar"]')
            xpath_botao_fechar.click()
            if return_chat_type:
                return chat_type, number
            else:
                return number

        except Exception as e:
            print(f'ocorreu um erro: {e}')
            return None

    def clean_chat(self):
        """Essa função irá limpar o chat que estiver aberto no momento."""
        self.find_button(Buttons_options.CHAT_MENU).click()
        time.sleep(0.2)
        self.find_button(Buttons_options.CLEAR_CHAT).click()
        time.sleep(0.2)
        self.find_button(Buttons_options.CLEAR_CONFIRM).click()
        time.sleep(0.2)

    def forward_message(self, index=-1, to=1):
        try:
            if len(to) > 5:
                raise ValueError(
                    "O Whatsapp somente encaminha 5 mensagens por vez.")
            self.open_message_menu(index)
            self.find_button(Buttons_options.FOWARD).click()
            time.sleep(0.5)
            self.find_button(Buttons_options.FOWARD).click()

            for contact in to:
                pyperclip.copy(contact)
                self.find_field(Field_options.FOWARD).send_keys(
                    Keys.CONTROL, 'v')
                time.sleep(0.2)
                self.find_field(Field_options.FOWARD).send_keys(Keys.ENTER)

            time.sleep(0.2)
            self.find_button(Buttons_options.FOWARD_CONFIRM).click()
            time.sleep(1)
            self.close_chat()
            time.sleep(0.2)

        except ValueError:
            logging.error(
                "A quantidade fornecida excedeu o limite de contatos para encaminhar")

        except Exception as e:
            logging.error("Ocorreu um erro: ", e)

    def click_message_option(self, message_element, option_selected=str):
        """Abre o menu da mensagem: Pega a lista de elementos de opções e clica no correspondente

        Args:
            option_selected (_type_, optional): _description_. Defaults to str.

        Raises:
            Exception: Acontece quando a opção inserida não é válida. Utilize msg_menu_options e selecione um argumento válido.

        """
        if option_selected in Msg_menu_options.LIST_MENU_OPTIONS:
            self.action.move_to_element(message_element).perform()
            time.sleep(0.2)
            message_menu_button = self.find_button(
                Buttons_options.MESSAGE_MENU)
            self.action.move_to_element(message_menu_button).click().perform()

            xpath = f"// *[contains(@class, 'iWqod') and contains(@class, '_1MZM5') and contains(@class, '_2BNs3') and @role='button' and @aria-label='{
                option_selected}']"
            element = self.browser.find_element(By.XPATH, xpath)
            print(f"Elemento encontrado: {element}")
            time.sleep(0.2)
            element.click()

        else:
            raise Exception(
                f"A opção '{option_selected}' não é válida. Utilize msg_menu_options e selecione um argumento válido.")

    def react_a_message(self, message_complete_element, reaction):
        # self.open_message_menu(message_complete_element)
        self.click_message_option(
            message_complete_element, Msg_menu_options.REACT)
        time.sleep(0.5)
        elements = self.browser.find_elements(
            By.XPATH, f"//div[contains(@class, 'tvf2evcx')]/div[@role='button']")
        element = elements[reaction]
        element.click()

        # Achar elementos web
        # Achar elementos web
        # Achar elementos web
        # Achar elementos web
        # Achar elementos web

    def find_message_complete_element(self, message_element):
        """Deve ser usado quando o chat estiver aberto

        Returns:
            WebElement: O elemento completo da mensagem, baseado no elemento da mensagem recebida,
            no elemento completo temos acesso as reações da mensagem
        """
        complete_element = message_element.find_element(
            By.XPATH, '../../../..')
        return complete_element

        # fazer o options e criar um def só chamado find_utils.

    def find_chat(self):
        """Deve ser usado para localizar o chat

        Returns:
            WebElement: O elemento do chat, utilizo para interações com toda a área do chat como mandar teclas 
            HOME para subir no chat e etc. 
        """
        return self.browser.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]')

    def find_reaction_in_a_message(self, message_Welement):
        return message_Welement.find_element(By.XPATH, ".//*[contains(@class, 'dhq51u3o')]")

    def find_messages(self, option=str):
        """Deve ser usado quando o chat estiver aberto

        Returns:
            list [WebElement]: O elemento das mensagens com base no modo escolhido.

        Opções:

            IN  = retorna apenas os elementos das mensagens recebidas. \n
            OUT = retorna apenas os elementos das mensagens enviadas.  \n
            ALL = retorna os elementos de todas as mensagens do chat.  \n
        """
        if option == Msg_options.IN:
            return self.browser.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]//div[contains(@class, 'copyable-text')]//div[@class='_21Ahp']//span[@class='_11JPr selectable-text copyable-text']")
        if option == Msg_options.OUT:
            return self.browser.find_elements(By.XPATH, "//div[contains(@class, 'message-out')]//div[contains(@class, 'copyable-text')]//div[@class='_21Ahp']//span[@class='_11JPr selectable-text copyable-text']")
        if option == Msg_options.ALL:
            return self.browser.find_elements(By.XPATH, "//div[contains(@class, 'message-out')]//div[contains(@class, 'copyable-text')]//div[@class='_21Ahp']//span[@class='_11JPr selectable-text copyable-text'] | //div[contains(@class, 'message-in')]//div[contains(@class, 'copyable-text')]//div[@class='_21Ahp']//span[@class='_11JPr selectable-text copyable-text']")
        else:
            raise Exception(
                "Ao utilizar o find_messages() é preciso um argumento válido. Utilize msg_options. e selecione o argumento")

    def find_field(self, option=str):
        if option == Field_options.MESSAGE:
            return self.browser.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
        if option == Field_options.TITTLE:
            return self.browser.find_element(By.XPATH, "//div[@class='to2l77zo gfz4du6o ag5g9lrv fe5nidar kao4egtt']")
        if option == Field_options.FOWARD:
            return self.browser.find_element(By.XPATH, '//p[@class="selectable-text copyable-text iq0m558w g0rxnol2"]')
        if option == Field_options.CONTACT:
            return self.browser.find_element(By.CLASS_NAME, "to2l77zo")
        if option == Field_options.REACTION:
            pass  # AINDA PRECISO FAZER!!!!!!!!!!!!!
            # AINDA PRECISO FAZER!!!!!!!!!!!!!
            # AINDA PRECISO FAZER!!!!!!!!!!!!!
            # AINDA PRECISO FAZER!!!!!!!!!!!!!
            # AINDA PRECISO FAZER!!!!!!!!!!!!!
            # AINDA PRECISO FAZER!!!!!!!!!!!!!
            # AINDA PRECISO FAZER!!!!!!!!!!!!!
            # AINDA PRECISO FAZER!!!!!!!!!!!!!
        else:
            raise Exception(
                "Ao utilizar o find_fields() é preciso um argumento válido. Utilize field_options. e selecione o argumento")

    def find_button(self, option=str):

        if option == Buttons_options.READMORE:
            return self.browser.find_elements(By.CLASS_NAME, 'read-more-button')

        if option == Buttons_options.ATTACH:
            return self.browser.find_element(By.CSS_SELECTOR, 'span[data-icon="attach-menu-plus"]')

        if option == Buttons_options.CHAT_MENU:
            return self.browser.find_element(By.XPATH, "//span[@data-icon='menu' and contains(@class, 'kiiy14zj')]")

        if option == Buttons_options.CLEAR_CHAT:
            return self.browser.find_element(By.XPATH, "//div[@class='iWqod' and @aria-label='Limpar conversa']")

        if option == Buttons_options.CLEAR_CONFIRM:
            return self.browser.find_element(By.XPATH, "//div[contains(@class, 'tvf2evcx') and contains(@class, 'm0h2a7mj') and contains(@class, 'lb5m6g5c') and contains(@class, 'j7l1k36l') and contains(@class, 'ktfrpxia') and contains(@class, 'nu7pwgvd') and contains(@class, 'p357zi0d') and contains(@class, 'dnb887gk') and contains(@class, 'gjuq5ydh') and contains(@class, 'i2cterl7') and contains(@class, 'i6vnu1w3') and contains(@class, 'qjslfuze') and contains(@class, 'ac2vgrno') and contains(@class, 'sap93d0t') and contains(@class, 'gndfcl4n')]")

        if option == Buttons_options.FOWARD:
            return self.browser.find_element(By.XPATH, '//button[@title="Encaminhar" and @type="button"]')

        if option == Buttons_options.FOWARD_CONFIRM:
            return self.browser.find_element(By.XPATH, "//div[contains(@class, 'lhggkp7q') and contains(@class, 'j2mzdvlq') and contains(@class, 'axi1ht8l') and contains(@class, 'mrtez2t4')]//span[@aria-label='Enviar']")

        if option == Buttons_options.MESSAGE_MENU:
            return self.browser.find_element(By.XPATH, '//span[@data-icon="down-context"]')

        else:
            raise Exception(
                "Ao utilizar o find_button() é preciso um argumento válido. Utilize buttons_options. e selecione o argumento")


# fazer depois
# relogios = self.browser.find_elements(
#            '//div[contains(@class, "message-in")]//span[@class="l7jjieqr" and text()="18:20"]')
#
