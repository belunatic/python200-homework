# --- Completions API ---

# API Q1
from dotenv import load_dotenv
from openai import OpenAI

#load from the .env
load_dotenv()
#create a OpenAI object
client = OpenAI()

# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "What is one thing that makes Python a good language for beginners?"}]
# )

# print(response.choices[0].message.content)
# print('\n')
# print(response.model)
# print('\n')
# print(response.usage)
# print('\n')

#API Q2
# prompt = "Suggest a creative name for a data engineering consultancy."
# temperatures = [0, 0.7, 1.5]

# for temp in temperatures:
#     response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "Suggest a creative name for a data engineering consultancy."}], 
#     temperature = temp
# )
#     print(f"Temperature: {temp} \n {response.choices[0].message.content}\n")

# '''
# What do you notice about how the outputs differ? Which temperature would you use if you needed a consistent, reproducible output?
# - Yes, the temp = 0 the name leaned more toward engineering terms. Looked and felt very rigid
# - temp = 0.7, involve more creativity and varied more and way better
# - temp = 1.5, gave me only one results, so it lack the creativity of precision on the task.
# - I would use the temp = 0.7
# '''

# API Q3
# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "Give me a one-sentence fun fact about pandas (the animal, not the library)."}],
#     n=3,
#     temperature=1.0
# )

# for res in response.choices:
#     print(f"{res.message.content} \n")

# API Q4
# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "Explain how neural networks work."}],
#     max_tokens = 15
# )

# print(response.choices[0].message.content)

# '''
# What happened, and why might you want to use max_tokens in a real application?
# - The response had a max of 14  words and the sentence was not completed.
# - The reason this is useful is because it help with keeping cost under control. Most model have a cut off of how many token you can use before getting charged.
# '''

#--- System Messages and Personas --