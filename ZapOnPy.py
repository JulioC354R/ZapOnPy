import os
import re
import time
import logging
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys


class ZOP:
    """Essa classe é responsável pelas interações diretas do selenium com o whatsapp-web, inclui funções de interação com mensagens, fazer o login, pegar números e etc."""

    def __init__(self, save_login=bool, headless=bool) -> None:
        '''Inicializar o webdriver com os dados de login ou não'''
        if save_login or headless:
            options = webdriver.ChromeOptions()
            # ao usar linux alterar para 'chromewithlogin/'
            userdir = 'c:\\chromewithlogin'
            if save_login:
                options.add_argument(f"--user-data-dir={userdir}")
            if headless:
                # Headless dando problema
                options.add_argument('--headless')  # Executar em modo headless
                # Desativar a aceleração de hardware (necessário para o modo headless em algumas plataformas)
                options.add_argument('--disable-gpu')
            self.browser = webdriver.Chrome(options=options)
        else:
            self.browser = webdriver.Chrome()
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
            time.sleep(5)
            WebDriverWait(self.browser, 10).until(
                EC.invisibility_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas'))
            )
            logging.info('QR code lido.')
            time.sleep(2)

        except Exception as e:
            logging.error(f"Ocorreu um erro \n{e}")

    def get_last_message(self):
        '''Pega a última mensagem em str e retorna ela, caso der erro, retorna None'''
        # Localiza todos os botões "Leia mais"

        try:
            self.click_on_readmore()
            # script para pegar ultima mensagem
            script = """
                var mensagens = document.querySelectorAll('#main div.copyable-text span[dir="ltr"]');
                return mensagens.length > 0 ? mensagens[mensagens.length - 1].innerText : null;
            """
            last_message = str(self.browser.execute_script(script))
            logging.info(f'Mensagem pega: {last_message}')
            return last_message
        except Exception as e:
            logging.error(f"Erro ao obter última mensagem: {e}")
            return None

    def get_all_messages(self):
        '''Pega uma grande quantidade de mensagens da conversa e retorna uma lista, caso der erro, retorna uma lista vazia'''
        try:

            # Apertar home para subir a página e carregar mais mensagens
            chat = self.find_chat()
            for _ in range(10):
                chat.send_keys(Keys.HOME)
                time.sleep(0.5)

            self.click_on_readmore()

            # Script para obter todas as mensagens
            script = """
                var mensagens = document.querySelectorAll('#main div.copyable-text span[dir="ltr"]');
                return Array.from(mensagens).map(function(mensagem) {
                    return mensagem.innerText;
                });
            """

            all_messages = self.browser.execute_script(script)
            # faz um list comprehention para criar uma lista com todas as messagens em formato string
            all_messages = [str(message)for message in all_messages]

            logging.info(f'Todas as mensagens pegas: {all_messages}')

            return all_messages

        except Exception as e:
            logging.error(f"Erro ao obter todas as mensagens: {str(e)}")
            return []

    def check_new_messages(self):
        '''Checa se tem novas mensagens e abre o chat que tem novas mensagens, retorna bool new_message'''
        try:
            new_message = self.find_new_message_icon()
            if new_message:
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

    # Achar elementos web

    def find_message_field(self):
        return self.browser.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')

    def find_readmore_buttons(self):
        return self.browser.find_elements(By.CLASS_NAME, 'read-more-button')

    def find_new_message_icon(self):
        return self.browser.find_elements(By.CLASS_NAME, '_2H6nH')

    def find_chat_new_message(self):
        return self.browser.find_element(By.XPATH, '//*[@id="pane-side"]//div[contains(@class, "_2H6nH")][1]')

    def find_chat(self):
        return self.browser.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]')

    def find_attach_icon(self):
        return self.browser.find_element(By.CSS_SELECTOR, 'span[data-icon="attach-menu-plus"]')

    def find_file_input(self):
        return self.browser.find_elements(By.CSS_SELECTOR, "input[type='file']")

    def find_tittle_box(self):
        return self.browser.find_element(By.XPATH, "//div[@class='to2l77zo gfz4du6o ag5g9lrv fe5nidar kao4egtt']")

    def find_contact_box(self):
        return self.browser.find_element(By.CLASS_NAME, "to2l77zo")
