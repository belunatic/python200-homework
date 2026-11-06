

from dotenv import load_dotenv
from openai import OpenAI
import json

#load from the .env
if load_dotenv():
    print("Loaded environment variables from .env file")
else:
    print("Warning: .env file not found. Make sure OPENAI_API_KEY is set.")

#OpenAI client
client = OpenAI()

def get_completion(messages, model="gpt-4o-mini", temperature=0.7):
    """
    Send a prompt to the model and return the assistant's text reply.
    This helper keeps our examples clean and focused on the prompt itself.

    attribute:
        message: a list of previous and current message sent as a prompt to OpenAI API client
        model: the model name being used
        temperature: the deterministic value for the model

    return:
        the content from the OpenAI API

    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=400
    )
    return response.choices[0].message.content

#system prompt
system_prompt = {'role': 'system', 'content': ''' You are a recruiter and helping someone get a job interview, they will share some information and material with you. As you review these material and information, I want you to Stay focus on a job application materials, always remind them to review and edit the output before submitting anywhere and lastly, but not least, acknowledge that you may not know the user's specific industry norms, and that the user should use their own judgment '''}

'''
explaining at least one deliberate choice you made in writing the system prompt and why?
- i choose recruiter as they have more access and entry way to getting an interview in the data engineering roles. Recruiter are mroe expose to the resume, cover letter and so on, so they might be a good judge of things'
'''

# parse LLM JSON responses
# function was created by AI
''' 
Due to many LLM return JSON as 
json
"""
[....]
"""

I created a function to remove the pre and post delimiters
'''
def parse_llm_json(response: str) -> list[dict]:
    ''' Strip leading and post character from a JSON response from OpenAI API Call
    
        attribute:
            response: A string contain the string that is going to be cleaned up and turn to JSON

        return:
            JSON response
    '''
    response = response.replace("```json", "")
    response = response.replace("```", "")
    return json.loads(response.strip())

# Task 2

def rewrite_bullets(bullets: list[str]) -> list[dict]:
    # Format the bullets into a delimited block
    bullet_text = "\n".join(f"- {b}" for b in bullets)

    prompt = f"""
    You are a professional resume coach helping a career changer.
    Rewrite each resume Bullet points below to be more specific, results-oriented, and compelling.
    Use strong action verbs. Do not invent facts that aren't implied by the original.

    Respond ONLY in a valid JSON list and nothing else. Each item should have two keys:
    "original" (the original bullet) and "improved" (your rewritten version).

    Bullet points:
    ```
    {bullet_text}
    ```
    """

    messages = [{"role": "user", "content": prompt}]

    try:
        response = get_completion(messages)
        results = parse_llm_json(response)
        # print(responses, results)
        print('\n')
        for result in results:
            print(f"{result['original']} \t {result['improved']}" )
    except json.JSONDecodeError:
        print("Error: result was not valid JSON")

#test
bullets = [
    "Helped customers with their problems",
    "Made reports for the management team",
    "Worked with a team to finish the project on time"
]

rewrite_bullets(bullets)