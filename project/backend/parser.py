from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup  
import random  
import time  
from fake_useragent import UserAgent

# Конфиг  
ANTI_CAPTCHA_API_KEY = "17e0b684051a23075a3aecacec79fa3e"  # Получить на anti-captcha.com  
user_agent = UserAgent()

# def get_image_keywords(image_path):  
#     client = OpenAI(base_url ='http://127.0.0.1:1234/v1', api_key='lm-studio')
#         prompt = open("dress.jpg")

#         response = client.chat.completions.create(
#         model='gemma-3-4b-it',
#         messages=[{'role': 'user', 'content': prompt}],
#         max_tokens=-1)

#         prompt.close()

#         return response.choices[0].message.content

def get_free_proxies():  
    proxies = [] 
    with open("freeproxies.txt", "r", encoding="utf-8") as file:
        proxies = file.readlines()
        proxies = [line.strip() for line in proxies] 
    return proxies  


def solve_captcha(image_url):
    pass

def setup_driver():  
    chrome_options = Options()  

    # Настройка прокси  
    #chrome_options.add_argument(f'--proxy-server={PROXY}')  

    # Случайный User-Agent  
    chrome_options.add_argument(f'--user-agent={UserAgent.chrome}')  

    # Скрытие автоматизации  
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  

    # Инициализация драйвера  
    driver = webdriver.Chrome(options=chrome_options)  

    # Инъекция Stealth.js  
    with open("project\\backend\\stealth.min.js", "r") as f:  
        js = f.read()  
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})  

    return driver  

def get_product_info():
    pass

def parse_products_id(url):  
    driver = setup_driver()  
    try:  
        driver.get(url)  

        # Обход всплывающих окон  
        WebDriverWait(driver, 15).until(  
            EC.invisibility_of_element_located((By.CLASS_NAME, "poplayer-content"))  
        )

        # Прокрутка для загрузки данных  
        for _ in range(3):  
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
            time.sleep(random.uniform(1.5, 3))

        # Сбор информации  
        products = driver.find_elements(By.CSS_SELECTOR, 'SnowSearchProductFeed_List__grid__wbj7b')
        products = driver.find_elements(By.CSS_SELECTOR, '[data-product-id]')

        # Сбор id товаров
        products_id = [product.get_attribute('data-product-id') for product in products]
        
        return products_id

    except Exception as e:  
        print(f"Ошибка: {e}")  
    finally:  
        driver.quit()  

# Поиск по ключевым словам  
keywords = "платье+для+девочки"

# Использование  
result = parse_products_id(f"https://aliexpress.com/wholesale?SearchText={keywords}")
print (result)