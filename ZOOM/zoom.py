# ALTERAR AS 3 CONSTANTES ABAIXO
# dados do zoom
link = 'https://ide-fgv-br.zoom.us/rec/share/GnPmwG4yu3423nGP0O8kBYLrg-8VOW1siAzS1oe6pwhL7q-WEXImDT_MpuvD9zZG.PhuMESAuBXDunkwN'
senha = '$X2RY$A@'

# Browser:
# 0 - Firefox
# 1 - Chrome
browser = 1

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary  # cleiton

import re

from bs4 import BeautifulSoup as bs

import requests as r
import time

if browser:
    driver = webdriver.Firefox()
else:
    driver = webdriver.Chrome('chromedriver')


def login(link, senha):
    driver.get(link)
    time.sleep(1)

    action = ActionChains(driver)
    campo_de_senha = driver.find_element('/html/body/div[1]/div[3]/div[2]/div[2]/div/form/div/div/input[1]')

    # precisa dar um click pra n achar que é bot
    campo_de_senha.click()

    # coloca a senha e aperta enterv
    campo_de_senha.send_keys(senha)
    campo_de_senha.send_keys(Keys.ENTER)


def cria_link():
    # Verifica se o chat carregou
    delay = 20  # seconds
    try:
        _ = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'user-name')))
    except:
        print("Loading took too much time!")

    # salva o código fonte da pagina
    pagina = driver.page_source
    parsed = bs(pagina)

    # procura pelo link do video, no player
    tag_link = parsed.find("div", attrs={"class": "player-view"})

    # separa o link por regex
    link = re.search('src=\"(http.+?)\" ', str(tag_link)).group(1)

    # altera o html fonte da página atraves de JS
    # substitui o título do chat por um link de download
    driver.execute_script(
        """document.querySelector("h2[class='title']").innerHTML="<a href=""" + link + """>Pimba!</a>";""")

    action = ActionChains(driver)
    pimba = driver.find_element('/html/body/div/section/div/div[3]/div[2]/div/div/h2')

    # depois desse comando o usuário precisa clicar em salvar como, selecionar a pasta e escolher o nome do arquivo
    action.context_click(pimba).perform()


login(link, senha)
cria_link()