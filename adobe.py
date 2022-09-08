import logging
from logging import exception

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
from bs4 import BeautifulSoup as Bs
import time
import os

# dados do zoom
link = 'https://ovly.adobeconnect.com/p7e5kwit0m38/'
user_mail = 'vanderleyy@gmail.com'
password = '@chevete'

def definir_navegador():
    # Definindo Browser:
    browser = int(input("Selecione o Navegador: (0) Chrome, (1) Firefox: "))
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
    return navegador

def abrir_navegador(link):
    try:
        # Abrindo o navegador
        print(f'-> Site: {link}')
        navegador.get(link)
        print(f'-> Aguarde por 3 segundos...')
        time.sleep(3)

        # digitar o site
        print(f'-> Verificando se o site foi aberto:')
    except NoSuchElementException:
        print(f'-> ###Site não encontrado###')


def executar_login(navegador, link, user_mail, password):
    try:
        _ = navegador.find_element(By.ID, "name")
        print(f'-> Site Encontrato!')
        # Aceitar os termos do site
        print(f'-> SESSAO: {navegador.session_id}')

        # Digitar Senha
        campo_email = navegador.find_element(By.ID, "name")
        campo_email.send_keys(user_mail)
        campo_senha = navegador.find_element(By.ID, "pwd")
        campo_senha.send_keys(password)
        campo_senha.send_keys(Keys.ENTER)

    except NoSuchElementException:
        print(f'-> ###Site não encontrado###')

def site_correto(navegador, link):
    try:
        _ = navegador.find_element(By.ID, "name")
        return True
    except NoSuchElementException:
        return False
        print(f'Elemento não encontrado')

def executar_player():
    try:
        time.sleep(15)
        botao_tocar = navegador.find_element(By.XPATH, "//iframe[@id='html-meeting-frame']")
        print(f'-> Site Encontrato!')
        print(f'-> Executando o Player')
        botao_tocar.click()

    except NoSuchElementException:
        print("-> Erro")

def criando_download():

    # verifique se o chat carregou
    print(f'-> Aguarde o Chat Ser Carregado - 15 segundos')
    time.sleep(10)
    print(f'-> Continuando.....')
    delay = 10

    try:
        elements = WebDriverWait(navegador, delay).until(ec.visibility_of_all_elements_located((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/h2[1]")))
        print("-> Elemento encontrado!")
        for element in elements:
            print(element.get_attribute("innerHTML"))
    except Exception as e:
        print(e)


    # salvar codigo-fonte
    pagina = navegador.page_source
    parsed = Bs(pagina)

    # procure pelo link do video, no player
    tag_link = parsed.find("div", attrs={"class": "player-view"})
    # separa o link por regex
    link = re.search('src=\"(http.+?)\" ', str(tag_link)).group(1)

    # altere o html fonte da pagina usando JS
    # troque o titulo do chat por um link de Download

    navegador.execute_script(
        """document.querySelector("h2[class='title']").innerHTML="<a href=""" + link + """>Pimba!</a>";""")
    action = ActionChains(navegador)
    pimba = navegador.find_element(By.XPATH, '/html/body/div/section/div/div[3]/div[2]/div/div/h2')

    # depois desse comando o usuário precisa clicar em salvar como, selecionar a pasta e escolher o nome do arquivo
    action.context_click(pimba).perform()


if __name__ == "__main__":
    navegador = definir_navegador()
    abrir_navegador(link)
    if site_correto(navegador, link):
        executar_login(navegador, link, user_mail, password)
    executar_player()
    criando_download()