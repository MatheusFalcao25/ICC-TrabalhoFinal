import csv
import json
import time
import sys
from selenium import webdriver
from selenium.common import __all__, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user = 'matheusfalcao@usp.br'
password = 'Abc123@@@'
home_page = 'https://investidor10.com.br/'


def scrapper_login(login_url, email, password):
    chrome_service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=chrome_service)
    driver.maximize_window()

    try:
        driver.get(login_url)
        time.sleep(3)
        account_menu_button = driver.find_element(By.XPATH, '/html/body/div[4]/header/div[1]/div/div[2]/a')
        account_menu_button.click()
        time.sleep(1)
        account_enter_button = driver.find_element(By.XPATH, '/html/body/div[4]/header/div[1]/div/div[2]/nav/ul/li[2]/a')
        account_enter_button.click()
        time.sleep(1)
        driver.find_element(By.NAME, 'email').send_keys(email)
        driver.find_element(By.NAME, 'password').send_keys(password)
        time.sleep(1)
        submit_button = driver.find_element(By.XPATH, '//*[@id="modal-sign"]/div/div[1]/form/div[3]/input')
        submit_button.click()
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, '//*[@id="modal-sign"]/div/div[1]/form/div[1]')
            return 0
        except NoSuchElementException:
            return 1

    except __all__:
        return -1


status = scrapper_login(home_page, user, password)
if status == 1:
    print('Login ok, iniciando webscrapper...')

    with open('acoes-listadas-b3.csv', newline='') as csv_file:
        table = csv.reader(csv_file, delimiter=',', quotechar='|')
        for line in table:
            print('Ticker: ' + line[0] + ' .Empresa: ' + line[1] + ' ...')

            chrome_service = Service(executable_path='chromedriver.exe')
            driver = webdriver.Chrome(service=chrome_service)
            url = f'https://investidor10.com.br/acoes/{json.loads(row[0])}'
            driver.get(url)

            wait = WebDriverWait(driver, 10)
            html_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#table-indicators-history')))
            button = driver.find_element(By.CLASS_NAME, 'btn-readmore')
            banner = driver.find_element(By.CLASS_NAME, 'banner-wallets')
            actions = ActionChains(driver)
            actions.move_to_element(banner).perform()
            button.click()

            table_data = []
            rows = html_table.find_elements(By.TAG_NAME, 'tr')
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                row_data = [cell.text for cell in cells]
                table_data.append(row_data)

            for row_data in table_data:
                print(row_data)

elif status == 0:
    sys.exit('Erro em tentar logar com usuário fornecido!')
elif status == -1:
    sys.exit('Erro interno na função de login, checar XPATH dos elementos!')
