# --- Completions API ---

# API Q1
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is one thing that makes Python a good language for beginners?"}]
)

print(response.choices[0].message.content)
print('\n')
print(response.model)
print('\n')
print(response.usage)
print('\n')