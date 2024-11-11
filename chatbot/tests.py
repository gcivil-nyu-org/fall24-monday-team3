from django.test import TestCase
import openai
from decouple import config

# Load the API key from environment variables
openai.api_key = config("OPENAI_API_KEY")


def test_openai_api():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, OpenAI!"}],
        )
        print("API Response:", response.choices[0].message["content"].strip())
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    test_openai_api()
