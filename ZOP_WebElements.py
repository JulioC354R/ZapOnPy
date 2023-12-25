from selenium.webdriver.common.by import By


# Exemplo para facilitar os comandos peguei a ideia do By do selenium.
#
#
class WElement:
    MESSAGES_IN = "MESSAGES_IN"


class Find:

    # Achar elementos Web

    def find(self, element=str):
        if element == "MESSAGES_IN":
            found = self.find_messages_in()
            return found

    def find_messages_in(self):
        """Deve ser usado quando o chat estiver aberto

        Returns:
            list [WebElement]: O elemento das mensagens que chegam, ou seja, apenas as mensagens recebidas.
        """
        return self.browser.find_elements(By.XPATH, '//div[contains(@class, "message-in")]//span[@class="_11JPr selectable-text copyable-text"]')


Zop = Find()

Zop.find(WElement.MESSAGES_IN)
