import openai
import os

# Load the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")


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
