# --- Completions API ---

# API Q1
from dotenv import load_dotenv
from openai import OpenAI

#load from the .env
load_dotenv()
#create a OpenAI object
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

#API Q2
prompt = "Suggest a creative name for a data engineering consultancy."
temperatures = [0, 0.7, 1.5]

for temp in temperatures:
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Suggest a creative name for a data engineering consultancy."}], 
    temperature = temp
)
    print(f"Temperature: {temp} \n {response.choices[0].message.content}\n")

'''
What do you notice about how the outputs differ? Which temperature would you use if you needed a consistent, reproducible output?
- Yes, the temp = 0 the name leaned more toward engineering terms. Looked and felt very rigid
- temp = 0.7, involve more creativity and varied more and way better
- temp = 1.5, gave me only one results, so it lack the creativity of precision on the task.
- I would use the temp = 0.7
# '''

# API Q3
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Give me a one-sentence fun fact about pandas (the animal, not the library)."}],
    n=3,
    temperature=1.0
)

for res in response.choices:
    print(f"{res.message.content} \n")

# API Q4
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Explain how neural networks work."}],
    max_tokens = 15
)

print(response.choices[0].message.content)

'''
What happened, and why might you want to use max_tokens in a real application?
- The response had a max of 14  words and the sentence was not completed.
- The reason this is useful is because it help with keeping cost under control. Most model have a cut off of how many token you can use before getting charged.
'''

#--- System Messages and Personas --

# System Q1

messages = [
    {"role": "system", "content": "You are a patient, encouraging Python tutor. You always explain things simply and end with a word of encouragement."},
    {"role": "user", "content": "I don't understand what a list comprehension is."}
]
messages_2 = [
    {"role": "system", "content": "You are 10 years old, teaching to a friend."},
    {"role": "user", "content": "I don't understand what a list comprehension is."}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

print('\n')
print(response.choices[0].message.content)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages_2,
)

print('\n')
print(response.choices[0].message.content)

'''
Add a comment noting what changed
- The coding examples used were different due to the change in role. One role demanded a 10 year old and another one was more of a professional role.
'''

# System Q2

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "My name is Jordan and I'm learning Python."},
    {"role": "assistant", "content": "Nice to meet you, Jordan! Python is a great choice. What would you like to work on?"},
    {"role": "user", "content": "Can you remind me what my name is?"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

print('\n')
print(response.choices[0].message.content)

'''
Why does the model know Jordan's name, even though it's stateless?
- Model is able to remember the name because the whole context of the message or previous messages are wrapped inside the message that is sent to the model in the request
'''

# --- Prompt Engineering ---
# Prompt Q1

reviews = [
    "The onboarding process was smooth and the team was welcoming.",
    "The software crashes constantly and support never responds.",
    "Great price, but the documentation is nearly impossible to follow."
]

for i,review in enumerate(reviews):
    prompt = [
        {"role": "system", "content": "classify the sentiment of this review below as positive, negative, or mixed only"},
        {"role": "user", "content": review}
    ]
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=prompt
    )

    print('\n')
    print(f"{i+1}. {response.choices[0].message.content}")


# Prompt Q2
prompt_content = '''
classify the sentiment of this review below as positive, negative, or mixed, then print out the review and sentiment as follows.
Example:
Review: "Fast shipping but the item arrived damaged."
Sentiment: mixed
'''

for review in reviews:
    prompt = [
        {"role": "system", "content": prompt_content},
        {"role": "user", "content": review}
    ]
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=prompt
    )

    print('\n')
    print(response.choices[0].message.content)

'''
Did adding one example change the format or consistency of the output compared to Q1?
- yes, it did, it is more descriptive and well formatted.
'''

#Prompt Q3
prompt_content = prompt_content = """
Classify the sentiment of each review as positive, negative, or mixed. Then print them out as follows

Examples:

Review: "The product arrived earlier than expected, the quality is excellent, and customer support was very helpful."
Sentiment: positive

Review: "The package arrived late, the item stopped working after a week, and customer service never responded."
Sentiment: negative

Review: "Fast shipping and great packaging, but the item arrived with a damaged screen."
Sentiment: mixed
"""

for review in reviews:
    prompt = [
        {"role": "system", "content": prompt_content},
        {"role": "user", "content": review}
    ]
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=prompt
    )

    print('\n')
    print(response.choices[0].message.content)

'''
Add a comment comparing all three approaches (zero-shot, one-shot, few-shot): When would you choose each one?
- Zero-shot, gave the result but it did not display the the reviews it was evaluating, so it create an extra work for the user or developer to know what review that sentiment is for.
- One-shot, gave the model and one example and it work great, it need more specific instruction but it was able to determine the output style.
- Few-shot, it act the same as One-Shot above, followed the same example but gave the mode  more options.

Where to use it?
- Zero-shot, is useful if the task is straight forward, a task that is frequently encountered in the training data; 1 + 1
- One-shot, helpful when task need more guidance or model struggle with ambiguity
- Few-shot, complex task requiring multiple examples to establish patterns
'''

# Prompt Q4

prompt_content = '''
Given a task, and before giving the final answer, explain your reasoning in 3–4 brief steps. Format your answer as follows:
Reasoning:
< list the reasoning or steps>
Final answer:
< final answer >
'''

messages = '''A data engineer earns $85,000 per year. She gets a 12% raise, then 6 months later
takes a new job that pays $7,500 more per year than her post-raise salary.
What is her final annual salary?'''

prompt = [
        {"role": "system", "content": prompt_content},
        {"role": "user", "content": messages}
    ]
response = client.chat.completions.create(
model="gpt-4o-mini",
messages=prompt
)

print('\n')
print(response.choices[0].message.content)

'''
Why does asking the model to reason step by step tend to improve accuracy on problems like this?
- This way you get to follow the model logic and see where it went wrong if it did
'''

#Prompt Q5

import json

prompt = [{ 'role':'user', 'content':"""
Classify the sentiment of the review and respond ONLY with valid JSON.
Keys: sentiment (positive/negative/mixed), confidence (0–1 scale), reason (one short sentence).

Review: "I've been using this tool for three months. It handles large datasets well, \
but the UI is clunky and the export options are limited."
"""
}]

response = client.chat.completions.create(
model="gpt-4o-mini",
messages=prompt
)

# Parse JSON safely
try:
    result = json.loads(response.choices[0].message.content)
    print("Parsed sentiment:", result["sentiment"])
    print("Confidence:", result["confidence"])
    print("Reason:", result["reason"])
except json.JSONDecodeError:
    print("Error: response was not valid JSON")


#Prompt Q6

user_text = "First boil a pot of water. Once boiling, add a handful of salt and the \
pasta. Cook for 8-10 minutes until al dente. Drain and toss with your sauce of choice."

prompt = f"""
You will be given text inside triple backticks.
If it contains step-by-step instructions, rewrite them as a numbered list.
If it does not contain instructions, respond with exactly: "No steps provided."

```{user_text}```
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
)

print(response.choices[0].message.content)