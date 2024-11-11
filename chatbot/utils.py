import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


def get_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"].strip()
