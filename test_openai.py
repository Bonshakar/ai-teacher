import openai
import os
from dotenv import load_dotenv

load_dotenv()  # .envファイル読み込み

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "こんにちは！"},
    ],
)

print(response.choices[0].message.content)
