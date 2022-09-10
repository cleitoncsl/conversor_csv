from selenium import webdriver
import pickle
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bs4 import BeautifulSoup as bs
import time
import os
import requests

# dados do zoom
link = 'https://ide-fgv-br.zoom.us/rec/share/qj_haBuI2cI6R0FUUzVg4UzfPOHBB6oNc6x4FmLj46w5M6UraIOos8jywZI0KwbB.Xolu3IuzhcrMTNp5'

# Definindo Browser:
browser = 0 #int(input("Selecione o Navegador: (0) Chrome, (1) Firefox: "))

# Matando os Processos

if browser == 0:
    os.system("taskkill /f /im chromedriver.exe")
else:
    os.system("taskkill /f /im geckodriver.exe")

if not browser:
    navegador = webdriver.Chrome('chromedriver')
else:
    navegador = webdriver.Firefox()

print(f'-> Navegador Selecionado: {navegador.name}')

def executar_login(link):
     # Abrindo o navegador
     print(f'-> Site: {link}')
     navegador.get(link)
     pickle.dump(navegador.get_cookies(), open("cookies.pkl", "wb"))
     cookies = pickle.load(open("cookies.pkl", "rb"))
     for cookie in cookies:
         navegador.add_cookie(cookie)

     print(f'-> Aguarde por 3 segundos...')
     time.sleep(3)
     #digitar o site
     print(f'-> Verificando se o site foi aberto:')
     try:

         print(f'-> Site Encontrato!')
     except NoSuchElementException:
         print(f'-> ###Site não encontrado###')
         print(f'-> SESSAO: {navegador.session_id}')


def criando_download():
    #verifique se o chat carregou
    print(f'-> Aguarde o Chat Ser Carregado - 10 segundos')
    time.sleep(10)
    print(f'-> Continuando.....')
    delay = 2 # segundos

    try:
        _ = WebDriverWait(navegador, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-name")))
        print("-> Elemento encontrado!")
    except TimeoutException:
        print("-> Elemento nao encontrado, o navegador será fechado.")
        navegador.quit()

    #salvar codigo-fonte
    pagina = navegador.page_source
    parsed = bs(pagina)

    #procure pelo link do video, no player
    tag_link = parsed.find("div", attrs={"class": "player-view"})
    # separa o link por regex
    link = re.search('src=\"(http.+?)\" ', str(tag_link)).group(1)

    #altere o html fonte da pagina usando JS
    #troque o titulo do chat por um link de Download

    navegador.execute_script(
        """document.querySelector("h2[class='title']").innerHTML="<a href=""" + link + """>Pimba!</a>";""")
    action = ActionChains(navegador)
    pimba = navegador.find_element(By.XPATH,'/html/body/div/section/div/div[3]/div[2]/div/div/h2')

    # depois desse comando o usuário precisa clicar em salvar como, selecionar a pasta e escolher o nome do arquivo
    action.context_click(pimba).perform()



executar_login(link)
criando_download()

