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
from selenium.common import exceptions
import time
from selenium.webdriver.common.keys import Keys


class ZOP:
    """Essa classe é responsável pelas interações diretas do selenium com o whatsapp-web, inclui funções de interação com mensagens, fazer o login, pegar números e etc."""

    def __init__(self, save_login=bool, headless=bool) -> None:
        '''Inicializar o webdriver com os dados de login ou não'''
        # configurando o caminho do chrome_driver
        driver_path = "./driver/chromedriver.exe"
        service = webdriver.ChromeService(executable_path=driver_path)

        if save_login or headless:
            options = webdriver.ChromeOptions()
            # ao usar linux alterar para 'chromewithlogin/'
            userdir = 'c:\\chromewithlogin'
            if save_login:
                options.add_argument(f"--user-data-dir={userdir}")
            if headless:
                # Headless dando problema
                # Executar em modo headless
                options.add_argument('--headless=new')
                # Desativar a aceleração de hardware (necessário para o modo headless em algumas plataformas)
                options.add_argument('--disable-gpu')
            self.browser = webdriver.Chrome(options=options, service=service)
        else:
            # iniciar sem nenhuma configuração
            self.browser = webdriver.Chrome(service=service)

        # inicializando action Chains
        self.action = ActionChains(self.browser)
        logging.info('Inicializando o navegador')
        self.bot_init()

    def close_browser(self):
        if self.browser is not None:
            self.browser.quit()
            self.browser = None

    def bot_init(self):
        '''Inicia o bot e espera até que o QR Code seja escaneado'''
        try:
            self.browser.get('https://web.whatsapp.com/')
            time.sleep(7)
            qrcode_xpath = '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas'
            qrcode = self.browser.find_element(By.XPATH, qrcode_xpath)
            qrcode.screenshot('qrcode.png')
            qr = QR()
            qr.ler_qrcode_imagem('qrcode.png')
            time.sleep(2)
            WebDriverWait(self.browser, 10).until(
                EC.invisibility_of_element_located((By.XPATH, qrcode_xpath))
            )
            logging.info('QR code lido.')
            time.sleep(7)

        except Exception as e:
            logging.error(f"Ocorreu um erro \n{e}")

    def get_messages_in(self):
        "Essa função pega apenas as mensagens recebidas"
        elements_message_in = self.find_messages_in()
        messages = []

        for message in elements_message_in:
            print(f'texto: {message.text}')
            messages.append(message.text)

        return messages

    def get_last_message(self):
        '''Pega a última mensagem em str e retorna ela, caso der erro, retorna None'''
        # Localiza todos os botões "Leia mais"

        try:
            self.click_on_readmore()
            time.sleep(0.5)
            last_message = self.get_messages_in()[-1]
            logging.info(f'Mensagem pega: {last_message}')
            return last_message
        except exceptions.NoSuchElementException:
            pass
        except Exception as e:
            logging.error(f"Erro ao obter última mensagem: {e}")
            return None

    def get_all_messages(self, scale=10):
        '''Pega uma grande quantidade de mensagens da conversa e retorna uma lista, caso der erro, retorna uma lista vazia
        O parametro scale recebe int, por padrão é 10. é quantidade de vezes que vai clicar na tecla HOME,
        assim pegando mais mensagens
        '''
        try:

            # Apertar home para subir a página e carregar mais mensagens
            chat = self.find_chat()
            for _ in range(scale):
                chat.send_keys(Keys.HOME)
                time.sleep(0.5)

            self.click_on_readmore()

            all_messages = self.get_messages_in()

            logging.info(f'Todas as mensagens pegas: {all_messages}')

            return all_messages

        except Exception as e:
            logging.error(f"Erro ao obter todas as mensagens: {str(e)}")
            return []

    def check_new_messages(self):
        '''Checa se tem novas mensagens e abre o chat que tem novas mensagens, retorna bool new_message'''
        try:
            new_message = self.find_new_message_icon()
            if new_message is not None:
                self.find_chat_new_message().click()
                time.sleep(0.5)
                logging.info('Novas mensagens foram encontradas')
                return new_message
            else:
                time.sleep(1)  # Aguarde um pouco antes de verificar novamente
        
        
        except Exception as e:
            logging.error(f"Erro ao encontrar novas mensagens: {e}")

    def send_message_on_chat(self, text=str, get_out=True):
        '''Envia uma mensagem quando o chat tá aberto, o get_out é para sair do chat ao enviar a mensagem'''
        self.false_typing(1.5)
        time.sleep(0.5)

        try:
            pyperclip.copy(text)
            time.sleep(0.5)
            message_field = self.find_message_field()
            message_field.send_keys(Keys.CONTROL, "v")

            time.sleep(0.5)
            # Pressiona "Enter" para enviar a mensagem
            message_field.send_keys(Keys.ENTER)
            logging.info('Mensagem enviada')
        except Exception as e:
            logging.error(f'Ocorreu um erro ao mandar a mensagem {e}')
        if get_out:
            self.close_chat()

    def false_typing(self, wait_seconds=float):
        '''Finge estar digitando pelo tempo de espera passado.
        Parâmetros:
        \nwait_seconds = float -> tempo de espera'''
        try:
            logging.info(f'Fingindo digitação por {wait_seconds} segundos.')
            message_field = self.find_message_field()
            message_field.send_keys('-')
            time.sleep(wait_seconds)
            message_field.send_keys(Keys.BACKSPACE)
        except Exception as e:
            logging.error(f'Ocorreu um erro: {e}')

    def send_midia(self, midia, text='', get_out=True, as_document=False):
        '''Envia uma foto / vídeo, com ou sem legenda. Parâmetros:
        \n midia   = str -> caminho da imagem/foto a ser enviada
        \n text    = str -> texto a ser enviado como legenda
        \n get_out = bool -> se ao terminar o comando deve sair do chat
        \n as_document = bool -> se True envia como um documento, se False envia como uma foto ou vídeo normal
        '''

        try:
            # pega o caminho real da mídia
            midia = os.path.abspath(midia)
            self.find_attach_icon().click()
            time.sleep(0.3)
            # Encontra o elemento de arquivo para enviar a mídia
            if as_document:
                # aqui ele envia como se fosse documento normal
                self.find_file_input()[0].send_keys(midia)
            else:
                # aqui envia como mídia
                self.find_file_input()[1].send_keys(midia)
            time.sleep(0.3)
            logging.info(f'Midia {midia} selecionada e pronta para enviar')
            time.sleep(0.5)
            # escreve o texto
            pyperclip.copy(text)
            tittle = self.find_tittle_box()
            tittle.send_keys(Keys.CONTROL, "v")
            time.sleep(0.5)
            tittle.send_keys(Keys.ENTER)
            logging.info('Imagem enviada com sucesso')
            # se True, sair do chat
            time.sleep(0.5)
            if get_out:
                self.close_chat()
        except Exception as e:
            logging.error(f'Ocorreu um erro: {e}')

    def search_contact(self, contact=str):
        '''procura o contato e entra na conversa'''
        try:
            self.find_contact_box().send_keys(contact, Keys.ENTER)
        except Exception as e:
            logging.error(f'Ocorreu um erro: {e}')

    def click_on_readmore(self):
        '''Função que clica em todos os "leia mais", para que as mensagens fiquem completas'''
        readmore_bottons = self.find_readmore_buttons()
        # Para cada botão, clique nele
        for botton in readmore_bottons:
            botton.click()

    def close_chat(self):

        try:
            self.find_message_field().send_keys(Keys.ESCAPE)
            logging.info('Fechando o chat')
        except:
            logging.info(f'Não conseguiu fechar o chat')

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
        self.find_chat_menu().click()
        time.sleep(0.2)
        self.find_clear_chat_option().click()
        time.sleep(0.2)
        self.find_clear_chat_confirm().click()
        time.sleep(0.2)

    def open_message_menu(self, index=-1):
        message = self.find_messages_in()[index]

        time.sleep(0.5)
        menu = self.find_message_menu(message)
        self.action.move_to_element(menu)
        menu.click()
        time.sleep(0.5)

    def forward_message(self, index=-1, to=None):
        try:
            if len(to) > 5:
                raise ValueError(
                    "O Whatsapp somente encaminha 5 mensagens por vez.")
            self.open_message_menu(index)
            self.find_foward_menu().click()
            time.sleep(0.5)
            self.find_foward_botton().click()

            for contact in to:
                pyperclip.copy(contact)
                self.find_foward_field().send_keys(Keys.CONTROL, 'v')
                time.sleep(0.2)
                self.find_foward_field().send_keys(Keys.ENTER)

            time.sleep(0.2)
            self.find_foward_send_botton().click()
            time.sleep(0.5)
            self.close_chat()
            time.sleep(0.2)

        except ValueError as ve:
            print(ve)

        except Exception as e:
            print(f"Ocorreu um outro erro: ", e)

        # Achar elementos web

    def find_messages_in(self):
        """Deve ser usado quando o chat estiver aberto

        Returns:
            list [WebElement]: O elemento das mensagens que chegam, ou seja, apenas as mensagens recebidas.
        """
        return self.browser.find_elements(By.XPATH, '//div[contains(@class, "message-in")]//span[@class="_11JPr selectable-text copyable-text"]')

    def find_message_field(self):
        """Deve ser usado quando o chat estiver aberto

        Returns:
            WebElement: O elemento da caixa de mensagem do chat, escrevo minhas mensagens usando
            pyperclip e send_keys(Keys.CTRL, "v")
        """
        return self.browser.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')

    def find_readmore_buttons(self):
        """Deve ser usado quando o chat estiver aberto

        Returns:
            list [WebElement]: O elemento do botão leia-mais, ao clicar nele vai estender todas as mensagens
            que são muito grandes e que são resumidas.
        """
        return self.browser.find_elements(By.CLASS_NAME, 'read-more-button')

    def find_new_message_icon(self):
        """Pode ser usado a qualquer momento

        Returns:
            int : O número de novas mensagens no elemento do icone de novas mensagens, 
            vai sempre pegar das mais antigas para as mais novas.

        Utilização:
            Use a função self.get_messages() passando a quantidade de novas mensagens multiplicado
            por -1 como index, assim vai pegar somente as novas mensagens daquele chat se tiver mais de uma
            podendo responder aos comandos 1 por 1

            OBS: ele encontra vários elementos mas a função [last()] no fim do xpath só retorna o ultimo
        """
        new_messages = self.browser.find_element(
            By.XPATH, "//div[@class='_2H6nH']//span[@aria-label='Não lidas'][last()]")
        quant = int(new_messages.text)
        return quant

    def find_chat_new_message(self):
        """Pode ser usado a qualquer momento

        Returns:
            WebElement: O elemento da conversa que tiver novas mensagens, vai sempre pegar das mais antigas 
            para as mais novas a fim de evitar tempo de espera muito grande das mensagens mais antigas.
        Utilização:
            Use a função .click para clicar no chat com novas mensagens (no último)

        OBS: ele encontra vários elementos mas a função [last()] no fim do xpath só retorna o ultimo
        """

        return self.browser.find_element(By.XPATH, '//*[@id="pane-side"]//div[contains(@class, "_2H6nH")][last()]')

    def find_chat(self):
        """Deve ser usado para localizar o chat

        Returns:
            WebElement: O elemento do chat, utilizo para interações com toda a área do chat como mandar teclas 
            HOME para subir no chat e etc. 
        """
        return self.browser.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]')

    def find_attach_icon(self):
        """Deve ser usado quando o chat estiver aberto

        Returns:
            WebElement: O elemento do ícone de clip, ao clicar abre o menu para seleção de attachs
        """
        return self.browser.find_element(By.CSS_SELECTOR, 'span[data-icon="attach-menu-plus"]')

    def find_file_input(self):
        """Deve ser usado após clicar no icone de clip (attach icon)

        Returns:
            list [WebElement]: lista de elementos para entrada de arquivos, seja imagens ou documentos.

        Utilize a função .send_keys("caminho do arquivo") para subir o arquivo ao input.
        Utilização baseado no índice:
            Indice 0 para enviar documento\n
            Indice 1 para enviar mídia\n
            Indice 2 para criação de figurinhas
        """
        return self.browser.find_elements(By.CSS_SELECTOR, "input[type='file']")

    def find_tittle_box(self):
        """Deve ser usado quando for mandar uma mídia ou documento.

        Returns:
            WebElement: O elemento de entrada de texto para título da mídia, eu uso o pyperclip
            para e .send_keys(Keys.CTRL, "v") para escrever, ao fim adicione uma linha como:
            elemento.send_keys(Keys.ENTER) que ele envia a mídia.
        """
        return self.browser.find_element(By.XPATH, "//div[@class='to2l77zo gfz4du6o ag5g9lrv fe5nidar kao4egtt']")

    def find_contact_box(self):
        """Pode ser usado a qualquer momento

        Returns:
            WebElement: O elemento de entrada de texto para pesquisar contatos, eu uso o pyperclip
            para e .send_keys(Keys.CTRL, "v") para escrever, ao fim adicione uma linha como:
            elemento.send_keys(Keys.ENTER) que ele abre o chat do contato.
        """
        return self.browser.find_element(By.CLASS_NAME, "to2l77zo")

    def find_chat_menu(self):
        """Deve ser usado enquanto o chat estiver aberto.

        Returns:
            WebElement: O elemento do botão menu do chat
        """
        return self.browser.find_element(By.XPATH, "//span[@data-icon='menu' and contains(@class, 'kiiy14zj')]")

    def find_clear_chat_option(self):
        """Deve ser usado após abrir o menu do chat (find_chat_menu)

        Returns:
            WebElement: O elemento do botão Limpar conversa
        """
        return self.browser.find_element(By.XPATH, "//div[@class='iWqod' and @aria-label='Limpar conversa']")

    def find_clear_chat_confirm(self):
        """Deve ser usado após selecionar a opção de limpar conversa

        Returns:
            WebElement: O elemento do botão Limpar conversa
        """
        return self.browser.find_element(By.XPATH, "//div[contains(@class, 'tvf2evcx') and contains(@class, 'm0h2a7mj') and contains(@class, 'lb5m6g5c') and contains(@class, 'j7l1k36l') and contains(@class, 'ktfrpxia') and contains(@class, 'nu7pwgvd') and contains(@class, 'p357zi0d') and contains(@class, 'dnb887gk') and contains(@class, 'gjuq5ydh') and contains(@class, 'i2cterl7') and contains(@class, 'i6vnu1w3') and contains(@class, 'qjslfuze') and contains(@class, 'ac2vgrno') and contains(@class, 'sap93d0t') and contains(@class, 'gndfcl4n')]")

    def find_message_menu(self, message):
        """Deve ser usado enquanto o chat estiver aberto e o mouse precisa passar por cima da mensagem
        para que abra o menu

        Args:
            message (WebElement): O elemento web da mensagem para que o menu seja aberto naquela mensagem em específico

        Returns:
            WebElement: O elemento do botão de envio da aba de encaminhar
        """
        self.action.move_to_element(message)
        message.click()
        return self.browser.find_element(By.XPATH, '//span[@data-icon="down-context"]')

    def find_foward_menu(self):
        """Deve ser usado após abrir o menu de mensagem (find_message_menu)

        Returns:
            WebElement: O elemento de seleção para encaminhar mensagens
        """
        return self.browser.find_element(By.XPATH, "//div[@class='iWqod _1MZM5 _2BNs3' and @role='button' and @aria-label='Encaminhar']")

    def find_foward_botton(self):
        """Deve ser usado após selecionar a mensagem

        Returns:
            WebElement: O elemento com o botão de encaminhar na área de seleção de mensagens
        """
        return self.browser.find_element(By.XPATH, '//button[@title="Encaminhar" and @type="button"]')

    def find_foward_field(self):
        """Deve ser usado após clicar no ícone de encaminhar

        Returns:
            WebElement: O elemento para escrever e procurar os contatos ao encaminhar, eu uso o pyperclip
            para e .send_keys(Keys.CTRL, "v") para escrever, ao fim adicione uma linha como:
            elemento.send_keys(Keys.ENTER) que ele seleciona o contato o qual vai encaminhar

        """
        return self.browser.find_element(By.XPATH, '//p[@class="selectable-text copyable-text iq0m558w g0rxnol2"]')

    def find_foward_send_botton(self):
        """Deve ser usado após selecionar os contatos de envio

        Returns:
            WebElement: O elemento do botão de envio da aba de encaminhar
        """
        return self.browser.find_element(By.XPATH, "//div[contains(@class, 'lhggkp7q') and contains(@class, 'j2mzdvlq') and contains(@class, 'axi1ht8l') and contains(@class, 'mrtez2t4')]//span[@aria-label='Enviar']")


# fazer depois
# relogios = self.browser.find_elements(
#            '//div[contains(@class, "message-in")]//span[@class="l7jjieqr" and text()="18:20"]')
#
