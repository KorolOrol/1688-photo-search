import requests

def send_image_recognition_request(image, url):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gemma-3-4b-it",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "ты должен давать ключевые слова для поиска товара на маркетплейсах по картинкам, которые тебе скидывают. ничего больше не добавляй"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image
                        }
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=payload)
    print("Received response")
    return response.json()['choices'][0]['message']['content']
