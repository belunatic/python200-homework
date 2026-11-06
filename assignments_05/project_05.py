

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
system_prompt = ''' You are a recruiter and helping someone get a job interview, they will share some information and material with you. As you review these material and information, I want you to Stay focus on a job application materials, always remind them to review and edit the output before submitting anywhere and lastly, but not least, acknowledge that you may not know the user's specific industry norms, and that the user should use their own judgment '''

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

# Task 3

def generate_cover_letter(job_title: str, background: str) -> str:
    prompt = f"""
    You write strong cover letter opening paragraphs for career changers.
    The paragraph should be 3-5 sentences: confident, specific, and free of clichés.

    Here are two examples of the style and tone you should match:

    Example 1:
    Role: Data Analyst at a healthcare nonprofit
    Background: Seven years as a registered nurse, recently completed a data analytics bootcamp.
    Opening: After seven years as a registered nurse, I've spent my career making decisions
    under pressure using incomplete information — which turns out to be excellent training for
    data analysis. I recently completed a data analytics program where I built dashboards
    tracking patient outcomes across departments. I'm excited to bring that combination of
    clinical context and technical skill to [Company]'s mission-driven work.

    Example 2:
    Role: Junior Software Engineer at a fintech startup
    Background: Ten years in retail banking operations, self-taught Python developer for two years.
    Opening: I spent a decade on the operations side of banking, watching technology decisions
    get made by people who had never processed a wire transfer or resolved a failed ACH batch.
    That frustration turned into curiosity, and two years of self-teaching Python later, I'm
    ready to be on the other side of those decisions. I'm applying to [Company] because your
    work on payment infrastructure is exactly where my domain expertise and new technical skills
    intersect.

    Now write an opening paragraph for this person:
    Role: {job_title}
    Background: {background}
    Opening:
    """

    messages = [{"role": "user", "content": prompt}]

    return get_completion(messages)

#Test 
job_title = "Junior Data Engineer"
background = "Five years of experience as a middle school math teacher; recently completed \
a Python course and built data pipelines using Pandas."
job_title_2 = "Data Engineer"
background_2 = "I have spent over 5 years as a web developer; I am currently working through a data engineering class and building pipeline using panda and python"


result = generate_cover_letter(job_title, background)
result_2 = generate_cover_letter(job_title_2, background_2)

print('\n')
print(result)
print('\n')
print(result_2)


'''
Why did you choose those particular examples? What does the few-shot pattern help control in the output?
- The examples here were already written for me in the task
- Few-shot pattern help the model / AI recognize pattern and deliver more accurate responses 
'''

# Task 4
def is_safe(text: str) -> bool:
    result = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
    flagged = result.results[0].flagged
    
    # print(result.results[0].categories)
    # Your code here: return True if safe, False if flagged, and print a message if flagged
    if not flagged:
        return True
    else:
        print('Sorry, but can you rephrase your statement')
        return False

#test
print('\n')
print(is_safe("You're a complete idiot and a waste of space."))
print('\n')
print(is_safe('I am in love with someone and I am shy'))

# Task 5

def run_chatbot():
    # 1. Initialize conversation history with your system prompt
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    print("=" * 50)
    print("Job Application Helper")
    print("=" * 50)
    print("I can help you with:")
    print("  1. Rewriting resume bullet points")
    print("  2. Drafting a cover letter opening")
    print("  3. Any other questions about your application")
    print("\nType 'quit' at any time to exit.\n")

    while True:
        user_input = input("You: ").strip()

        # 2. Handle exit
        if user_input.lower() in {"quit", "exit"}:
            print("\nJob Application Helper: Good luck with your applications!")
            break

        # 3. Skip empty input
        if not user_input:
            continue

        # 4. Run moderation check before doing anything else
        if not is_safe(user_input):
            continue  # is_safe() already printed the warning message

        # 5. Check if the user wants to rewrite bullets
        #    (hint: look for keywords like "bullet" or "resume" in user_input.lower())
        if "bullet" in user_input.lower() or "resume" in user_input.lower():
            print("\nJob Application Helper: Paste your bullet points below, one per line.")
            print("When you're done, type 'DONE' on its own line.\n")
            raw_bullets = []
            while True:
                line = input().strip()
                if line.upper() == "DONE":
                    break
                if line:
                    raw_bullets.append(line)
            # YOUR CODE: call rewrite_bullets() and print the results
            rewrite_bullets(raw_bullets)

        # 6. Check if the user wants a cover letter
        elif "cover letter" in user_input.lower():
            job_title = input("Job Application Helper: What is the job title? ").strip()
            background = input("Job Application Helper: Briefly describe your background: ").strip()
            # YOUR CODE: call generate_cover_letter() and print the result
            result = generate_cover_letter(job_title, background)
            print('\n')
            print(result)

        # 7. Otherwise, handle it as a regular chat turn
        else:
            # YOUR CODE:
            # - Append the user's message to `messages`
            messages.append({'role': 'user', 'content': user_input})
            # - Call get_completion(messages)
            print('----')
            print(messages)
            print('----')
            response = get_completion(messages)
            # - Print the reply
            print(response)
            # - Append the reply to `messages` as an assistant message
            messages.append({'role': 'assistant', 'content': response})
            #check message length
            print('\n')
            print('Message length: ', len(messages))
            pass


if __name__ == "__main__":
    run_chatbot()