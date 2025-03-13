from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium import webdriver
from bs4 import BeautifulSoup
import random

""" 
НЕ ЗАПУСКАТЬ!
прокси ещё не подключены.
может забанить на алике.
"""
class AliexpressParser:
    def __init__(self):
        self.user_agent = UserAgent()
        self.driver = self._setup_driver()

    def __del__(self):
        self.driver.quit()

    def _setup_driver(self):
        chrome_options = Options()

        # Настройка прокси
        #chrome_options.add_argument(f'--proxy-server=93.171.157.249:8080')

        # Случайный User-Agent
        chrome_options.add_argument(f'--user-agent={UserAgent.chrome}')

        # Скрытие автоматизации
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Инициализация драйвера
        newDriver = webdriver.Chrome(options=chrome_options)

        # Инъекция Stealth.js
        with open("project\\backend\\ml\\stealth.min.js", "r") as f:
            js = f.read()
        newDriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

        return newDriver

    def solve_captcha():
        pass

    def parse_products_cards(self, keywords):
        try:
            self.driver.get(f"https://aliexpress.com/wholesale?SearchText={keywords}")

            # Обход всплывающих окон
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "poplayer-content"))
            )
            soup = BeautifulSoup(self.driver.page_source, features="html.parser")

            products = self.driver.find_elements(By.CSS_SELECTOR, '[data-product-id]')      

            # Сбор id товаров
            products_cards = [product.text for product in products]
            
            return products_cards

        except Exception as e:
            print(f"Ошибка(id): {e}")

# пример использования
# keywords = send_image_recognition_request('project\\backend\\ml\\test.jpg', 'http://127.0.0.1:1234')
# parser = AliexpressParser()

# products_cards = parser.parse_products_cards(keywords)

# for i in products_cards:
#     print(i.split("\n"))
