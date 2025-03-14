from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium import webdriver
from bs4 import BeautifulSoup
import re 
import time
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
    
    def parse_products_text(self, products):
        parsed_products = []
        
        for product in products:
            parts = [p.strip() for p in product.split('\n') if p.strip()]
            product_data = {
                'discount': None,
                'new_price': None,
                'rating': None,
                'bought_count': None,
                'name': None,
                'additional': None,
                'link': None
            }
            
            current_index = 0
            
            # Проверяем наличие метки скидки (может быть изменена в будущем)
            if parts[0] == 'НИХАО СКИДКА':
                current_index += 1  # Пропускаем метку

            # Обрабатываем цену и скидку
            while current_index < len(parts):
                part = parts[current_index]
                
                # Проверяем наличие цены со скидкой (новый формат: "X XXX ₽-YY%")
                price_discount_match = re.match(r'^(\d[\d ]*)₽-(\d+)%$', part.replace(' ', ''))
                if price_discount_match:
                    product_data['new_price'] = price_discount_match.group(1).replace(' ', '')
                    product_data['discount'] = price_discount_match.group(2)
                    current_index += 1
                    break
                
                # Проверяем обычную цену
                price_match = re.match(r'^(\d[\d ]*)₽$', part.replace(' ', ''))
                if price_match:
                    product_data['new_price'] = price_match.group(1).replace(' ', '')
                    current_index += 1
                    break
                
                current_index += 1

            # Обрабатываем рейтинг
            if current_index < len(parts) and re.match(r'^\d\.\d$', parts[current_index]):
                product_data['rating'] = parts[current_index]
                current_index += 1

            # Обрабатываем количество покупок
            if current_index < len(parts) and 'купили' in parts[current_index]:
                product_data['bought_count'] = re.search(r'\d+', parts[current_index]).group()
                current_index += 1

            # Собираем название товара
            name_parts = []
            while current_index < len(parts):
                part = parts[current_index]
                if part in ['бесплатно', 'до 14 дней', 'Рекомендуем']:
                    product_data['additional'] = part
                    current_index += 1
                    break
                name_parts.append(part)
                current_index += 1
            
            product_data['name'] = ' '.join(name_parts) if name_parts else None

            parsed_products.append(product_data)
        
        return parsed_products

    def parse_products_cards(self, keywords):
        try:
            print("Received keywords")
            self.driver.get(f"https://aliexpress.com/wholesale?SearchText={keywords}")

            # Обход всплывающих окон
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "poplayer-content"))
            )
            soup = BeautifulSoup(self.driver.page_source, features="html.parser")
            
            time.sleep(10)

            products_cards = self.driver.find_elements(By.CSS_SELECTOR, '[data-product-id]') 
            products_id = [product.get_attribute('data-product-id') for product in products_cards]
            products_cards = [i.text for i in products_cards]
            products_cards = self.parse_products_text(products_cards)

            for i in range(len(products_cards)):
                products_cards[i]['link'] = 'https://aliexpress.com/item/' + str(products_id[i]) + '.html'
            
            print(products_cards)
            return products_cards

        except Exception as e:
            print(f"Ошибка: {e}")

# пример использования
# keywords = send_image_recognition_request('project\\backend\\ml\\test.jpg', 'http://127.0.0.1:1234')
# parser = AliexpressParser()

# products_cards = parser.parse_products_cards(keywords)

# print(products_cards)
