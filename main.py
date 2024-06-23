import csv
import json
import time
import sys
from selenium import webdriver
from selenium.common import __all__, NoSuchElementException         #Importa condições para tratar no excepts
from selenium.webdriver.chrome.service import Service               #Importa o serviço que será utilizado para carregar o chromedriver.exe
from selenium.webdriver.common.by import By                         #Importa método para buscar elementos no html
from selenium.webdriver.common.action_chains import ActionChains    #Importa funcionalidade de scroll da pagina
from selenium.webdriver.support.ui import WebDriverWait             #Importa funcionalidade de esperar a pagina web carregar
from selenium.webdriver.support import expected_conditions as EC    #Importa condições uteis para o tratamento da pagina

# Credenciais e URL inicial
user = 'matheusfalcao@usp.br'
password = 'Abc123@@@'
home_page = 'https://investidor10.com.br/'


# Função para fazer login no site
def scrapper_login(login_url, email, password):
    chrome_service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=chrome_service)
    driver.maximize_window()

    try:
        # Abre a página de login
        driver.get(login_url)
        time.sleep(3)

        # Clica no menu de conta
        account_menu_button = driver.find_element(By.XPATH, '/html/body/div[4]/header/div[1]/div/div[2]/a')
        account_menu_button.click()
        time.sleep(1)

        # Clica no botão de entrar
        account_enter_button = driver.find_element(By.XPATH, '/html/body/div[4]/header/div[1]/div/div[2]/nav/ul/li[2]/a')
        account_enter_button.click()
        time.sleep(1)

        # Preenche os campos de email e senha
        driver.find_element(By.NAME, 'email').send_keys(email)
        driver.find_element(By.NAME, 'password').send_keys(password)
        time.sleep(1)

        # Submete o formulário de login
        submit_button = driver.find_element(By.XPATH, '//*[@id="modal-sign"]/div/div[1]/form/div[3]/input')
        submit_button.click()
        time.sleep(2)

        # Verifica se há mensagem de erro de login
        try:
            driver.find_element(By.XPATH, '//*[@id="modal-sign"]/div/div[1]/form/div[1]')
            return 1
        except NoSuchElementException:
            return 0

    except __all__:
        return -1


# Executa a função de login
status = scrapper_login(home_page, user, password)
if status == 1:
    print('Login ok, iniciando webscrapper...')

    # Abre o arquivo CSV contendo os dados das ações
    with open('acoes-listadas-b3.csv', newline='') as csv_file:
        table = csv.reader(csv_file, delimiter=',', quotechar='|')
        for line in table:
            print('Ticker: ' + line[0] + ' .Empresa: ' + line[1] + ' ...')

            # Cria um novo WebDriver para cada ação
            chrome_service = Service(executable_path='chromedriver.exe')
            driver = webdriver.Chrome(service=chrome_service)
            url = f'https://investidor10.com.br/acoes/{json.loads(line[0])}'
            driver.get(url)

            # Espera até que a tabela de indicadores esteja presente
            wait = WebDriverWait(driver, 10)
            html_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#table-indicators-history')))

            # Localiza e clica no botão para carregar mais dados
            button = driver.find_element(By.CLASS_NAME, 'btn-readmore')
            banner = driver.find_element(By.CLASS_NAME, 'banner-wallets')
            actions = ActionChains(driver)
            actions.move_to_element(banner).perform()
            button.click()

            # Extrai os dados da tabela
            table_data = []
            rows = html_table.find_elements(By.TAG_NAME, 'tr')
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                row_data = [cell.text for cell in cells]
                table_data.append(row_data)

            # Imprime os dados da tabela
            for row_data in table_data:
                print(row_data)

# Tratamento de erros de login
elif status == 0:
    sys.exit('Erro em tentar logar com usuário fornecido!')
elif status == -1:
    sys.exit('Erro interno na função de login, checar XPATH dos elementos!')
