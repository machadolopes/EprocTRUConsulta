import time
import requests
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import smtplib
import email.message
import config

def send_email(resultado):
        #email_sender = config.email_sender
        #email_password = config.password
        #email_recipient = config.email_recipient
        subject = 'Novas intimações TRU'
        body = resultado
       
        msg = email.message.Message()
        msg['From'] = config.email_sender
        msg['To'] = config.email_recipient
        msg['Subject'] = subject
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(body)
        s= smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login(config.email_sender, config.email_password)
        s.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))
        print('Email enviado com sucesso')

def consulta_novas_intimacoes_TRU():
    #def login(username, password):
    url=config.url
    username = config.username
    password = config.password
    # Inicializa o navegador
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach",True)
    #options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    # Abre a página de login
    response=requests.get(url)
    if response.status_code==200:
        driver.get(url)
        print("Conexão estabelecida...")
    else:
        print("servidor fora do ar. Tente mais tarde.")
        driver.quit

    time.sleep(1)
    # Encontra os campos de login e senha
    username_input = driver.find_element(by=By.ID,value="txtUsuario")
    password_input = driver.find_element(by=By.ID,value="pwdSenha")
    print("Fazendo login...")

    # Preenche os campos de login e senha
    username_input.send_keys(username)
    password_input.send_keys(password)

    # Clica no botão de login
    driver.find_element(by=By.ID,value="sbmEntrar").click()
    time.sleep(1)
    # Seleciona perfil do usuário
    perfil_input = driver.find_element(by=By.ID,value="tr1")
    perfil_input.click()
    print("Selecionando perfil de usuário...")
    time.sleep(4)
    #aciona menu dropdown
    seleciona_menu_dropdown = driver.find_element(by=By.CSS_SELECTOR, value="#main-menu > li:nth-child(5) > a > span.menu-item-text")
    seleciona_menu_dropdown.click()
    print("Entrando no gerenciamento de processos...")
    time.sleep(2)
    #Seleciona gerenciamento de processos
    seleciona_gerenciamento_processos = driver.find_element(by=By.CSS_SELECTOR, value="#menu-ul-38 > li:nth-child(1) > a > span.menu-item-text")
    seleciona_gerenciamento_processos.click()

    time.sleep(2)
    # define o dia de hoje e seleciona data de intimação
    currentDate = date.today().strftime("%d/%m/%Y")
    seleciona_data_intimacao = driver.find_element(by=By.ID, value="txtDataIntimacao")
    seleciona_data_intimacao.send_keys('10/11/2023')
    print("Pesquisandos novas intimações hoje...")
    time.sleep(1)
    #seleciona o menu dropdown dos órgãos julgadores
    dropdown = driver.find_element(by=By.CSS_SELECTOR,value="#frmGerenciamento > div:nth-child(5) > div:nth-child(5) > div > button > div")
    time.sleep(2)
    dropdown.click()
    time.sleep(4)
    print("Selecionando órgãos julgadores da TRU...")
    preenche_orgao_julgador= driver.find_element(by=By.CSS_SELECTOR, value="#frmGerenciamento > div:nth-child(5) > div:nth-child(5) > div > div > div > input[type=text]")
    preenche_orgao_julgador.send_keys("TRU")
    time.sleep(1)
    seleciona_todos= driver.find_element(by=By.CSS_SELECTOR, value="#frmGerenciamento > div:nth-child(5) > div:nth-child(5) > div > div > ul > li.ms-select-all > label > input[type=checkbox]")
    time.sleep(2)
    seleciona_todos.click()
    #seleciona_todos = driver.find_element(by=By.CLASS_NAME, value="ms-select-all")
    #seleciona_todos.click()
    time.sleep(4)
    #faz consulta
    print("Pesquisando...")
    pressiona_botao_consultar = driver.find_element(by=By.CSS_SELECTOR, value='#btnConsultar')
    driver.execute_script("arguments[0].click();", pressiona_botao_consultar)
    #driver.find_element(by=By.CLASS_NAME, value='infraButton')
    time.sleep(5)
    #verifica se retornaram resultados
    #lblContato
    if driver.page_source.__contains__('Nenhum processo encontrado'):
        resultado_consulta = 'Pesquisa sem resultados ' 
        print("Pesquisa sem resultados")
        send_email(resultado_consulta)
        st.text_area(resultado_consulta)
    else:
    #seleciona tabela com resultados
        time.sleep(5)
        resultados =driver.find_elements(by=By.XPATH, value='//*[@id="tabelaProcessos"]/tbody/tr/td[2]/a')
        print("pesquisa com resultados...")
       
        for item in resultados:
            novas_intimacoes_TRU = item.text.encode('utf-8').decode('utf-8')
            msg = "Novas intimações em {1} nos processos {2}".format(currentDate,novas_intimacoes_TRU)
            print(item.text.encode('utf-8').decode('utf-8'))
            continue
    return msg

msg_email=consulta_novas_intimacoes_TRU() 
send_email(msg_email) 
      




    


        
        
        



    


    # Exemplo de uso




