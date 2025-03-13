from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium import webdriver
from bs4 import BeautifulSoup
import random
import time
import re 
""" 
НЕ ЗАПУСКАТЬ!
прокси ещё не подключены.
может забанить на алике.
"""
class AliexpressParser:
    def __init__(self):
        self.user_agent = UserAgent()
        self.ANTI_CAPTCHA_API_KEY = "17e0b684051a23075a3aecacec79fa3e"
        self.driver = self._setup_driver()

    def __del__(self):
        self.driver.quit()

    def _setup_driver(self):
        chrome_options = Options()

        # Настройка прокси
        #chrome_options.add_argument(f'--proxy-server={PROXY}')

        # Случайный User-Agent
        chrome_options.add_argument(f'--user-agent={UserAgent.chrome}')

        # Скрытие автоматизации
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

<<<<<<< HEAD
def get_free_proxies():  
    proxies = [] 
    with open("freeproxies.txt", "r", encoding="utf-8") as file:
        proxies = file.readlines()
        proxies = [line.strip() for line in proxies] 
    return proxies  

=======
        # Инициализация драйвера
        newDriver = webdriver.Chrome(options=chrome_options)
>>>>>>> 03f57d60952ac46c6ee7be02c5022def51ccce60

        # Инъекция Stealth.js
        with open("project\\backend\\stealth.min.js", "r") as f:
            js = f.read()
        newDriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

        return newDriver
    
    def get_image_keywords():
        pass

    def get_free_proxies():
        pass

    def solve_captcha():
        pass

    def parse_products_id(self, keywords):
        try:
            self.driver.get(f"https://aliexpress.com/wholesale?SearchText={keywords}")

            # Обход всплывающих окон
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "poplayer-content"))
            )

            products = self.driver.find_elements(By.CSS_SELECTOR, '[data-product-id]')      

            # Сбор id товаров
            products_id = [product.get_attribute('data-product-id') for product in products]
            
            return products_id

        except Exception as e:
            print(f"Ошибка(id): {e}")

    #TODO: Добавить в функцию парсинг остальных полей
    def parse_product_info(self, product_id):
        try:
            self.driver.get(f"https://aliexpress.com/item/{product_id}.html")

            #сбор информации
            soup = BeautifulSoup(self.driver.page_source, features="html.parser")
            product_name = soup.find(attrs={"data-header-mark": "true"})
            product_price = soup.find(attrs={"data-spm":"title_floor"})

            return product_name.text

        except Exception as e:
            print(f"Ошибка(info): {e}")


parser = AliexpressParser()
keywords = "iphone 13"

products_id_list = parser.parse_products_id(keywords)

for i in products_id_list:
    print(parser.parse_product_info(i), i)