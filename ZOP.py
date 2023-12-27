import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# Crie uma instância do navegador Chrome
driver = webdriver.Chrome()
time.sleep(5)

# Execute algum código JavaScript para definir o conteúdo da área de transferência
js_code = """
var dummy = document.createElement("input");
document.body.appendChild(dummy);
dummy.setAttribute("id", "dummy_id");
document.getElementById("dummy_id").value = "💁👌🎍😍";
dummy.select();
document.execCommand("copy");
document.body.removeChild(dummy);
"""
driver.execute_script(js_code)
driver.get("http://www.google.com")

# Cole o conteúdo da área de transferência em um campo de entrada (pode ser um campo de pesquisa)
campo_input = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
time.sleep(1)
campo_input.send_keys(Keys.CONTROL + 'v')
campo_input.send_keys(Keys.ENTER)

time.sleep(300)
# Restante do seu código Selenium...

# Feche o navegador
driver.quit()
