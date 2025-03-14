from openai import OpenAI
import base64

def send_image_recognition_request(image, model_name):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    with open(image, "rb") as image:
        base64_string = base64.b64encode(image.read()).decode("utf-8")

    base64_value = f"data:image/png;base64,{base64_string}"

    response = client.chat.completions.create(
        model='gemma-3-4b-it',
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "ты должен давать ключевые слова для поиска товара на маркетплейсах по картинкам, которые тебе скидывают. ничего больше не добавляй"},
                {"type": "image_url", "image_url": {"url": base64_value}}
            ]}
        ],
        stream=False
    )

    output = response.choices[0].message.content

    return output
