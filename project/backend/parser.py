import requests  
from bs4 import BeautifulSoup  
import random  
import time  
from fake_useragent import UserAgent

# Конфиг  
PROXY_LIST_URL = "https://free-proxy-list.net/"  
ANTI_CAPTCHA_API_KEY = "17e0b684051a23075a3aecacec79fa3e"  # Получить на anti-captcha.com  
user_agent = UserAgent()

def get_image_keywords(image_path):  
    client = OpenAI(base_url ='http://127.0.0.1:1234/v1', api_key='lm-studio')
        prompt = open("dress.jpg")

        response = client.chat.completions.create(
        model='gemma-3-4b-it',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=-1)

        prompt.close()

        return response.choices[0].message.content

def get_free_proxies():  
    response = requests.get(PROXY_LIST_URL)  
    soup = BeautifulSoup(response.text, 'html.parser')  
    proxies = []  
    for row in soup.select('table.table tbody tr'):  
        cells = row.find_all('td')
        if cells[4].text == 'elite proxy' and cells[6].text == 'yes':  
            proxies.append(f"{cells[0].text}:{cells[1].text}")  
    return proxies  

def solve_captcha(image_url):  
    data = {
        "clientKey": ANTI_CAPTCHA_API_KEY,  
        "task": {"type": "ImageToTextTask", "body": image_url}  
    }  
    response = requests.post('https://api.anti-captcha.com/createTask', json=data).json()  
    task_id = response.get('taskId')  
    time.sleep(10)  # Ожидание решения  
    result = requests.get(f'https://api.anti-captcha.com/getTaskResult/{task_id}').json()  
    return result.get('solution', {}).get('text')  

def parse_aliexpress(product_url):  
    #proxies = get_free_proxies()  
    session = requests.Session(product_url)
    headers = {
        "User-Agent": user_agent.random,  
        "Accept-Language": "ru-RU,ru;q=0.9",
        "path": "/api/v1/analytics/search"
    }

    for attempt in range(5):  
        #proxy = {'http': f'http://{random.choice(proxies)}'}  
        try:  
            response = requests.get(product_url, headers=headers, timeout=15)  
            # if "captcha" in response.text:  
            #     # Обход капчи  
            #     captcha_url = BeautifulSoup(response.text, 'html.parser').find('img', {'id': 'captcha'})['src']  
            #     solution = solve_captcha(captcha_url)  
            #     # Повтор запроса с решением  
            #     response = requests.get(product_url, headers=headers, proxies=proxy, params={'captcha': solution})  
            #     print('captcha')
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup

        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(random.randint(2, 7))
    
    return None

# # Поиск по ключевым словам  
keywords = get_image_keywords("dress.jpg").replace(" ", "+")

# Использование  
result = parse_aliexpress(f"https://aliexpress.ru/wholesale?SearchText={keywords}")

print(result)