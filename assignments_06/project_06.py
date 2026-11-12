from dotenv import load_dotenv
import os
from pathlib import Path
from llama_index.core import Settings,SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

if load_dotenv():
    print("API key loaded successfully.")
else:
    print("Warning: could not load API key. Check your .env file.")

#An assert statement stops the program early with a clear error message if a condition is not met
docs_dir = Path("./resources/groundwork_docs")
assert docs_dir.exists(), f"Document directory not found: {docs_dir}"

#load all documents
docs = SimpleDirectoryReader('./resources/groundwork_docs').load_data()

#print length of files loaded and their names
print('\n', '-' *30)
print(f"{len(docs)} were loaded")
print('\n')
for doc in docs:
    print(doc.metadata['file_name'])

# Building the Index and query Engine
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.llm = OpenAI(model="gpt-4o-mini")

# Build a vector index automatically (handles chunking + embeddings)
index = VectorStoreIndex.from_documents(docs)

#query engine
query_engine = index.as_query_engine(similarity_top_k=3)

print('\n', '-' *30)
print('Index built successfully. Ready to answer questions.')

# query
questions = [
    "What are Groundwork's hours on weekends?",
    "Do you offer any dairy-free milk options?",
    "How does the loyalty program work?",
    "How did Groundwork Coffee get started?",
    "Do you offer catering or wholesale orders?",
]

# for q in questions:
#     print('\n', '*' *30)
#     print(f"\nQ: {q}")
#     response = query_engine.query(q)
#     print("A:", response)
#     print('\n')
    
#     for node_with_score in response.source_nodes:
#         print(f"Node ID: {node_with_score.node.node_id}")
#         print(f"Similarity Score: {node_with_score.score:.4f}")
#         print(f"Text Snippet: {node_with_score.node.get_content()[:150]}...")
#         print("-" * 30)

#     print('\n')

'''
did the assistant sound confident and accurate? Did any of the answers surprise you?
- Yes, assistance sounded confident and accurate.
- one thing surprised me on the "dairy-free question", it ranked the seasonal_specials.txt high in similarity score than the  menu which stated the different dairy-free milk. i notice how it look for keywords and then find semantic meaning after.
'''

q = 'What should I know?'
print('\n', '*' *30)
print(f"\nQ: {q}")
response = query_engine.query(q)
print("A:", response)
print('\n')

for node_with_score in response.source_nodes:
    print(f"Node ID: {node_with_score.node.node_id}")
    print(f"Similarity Score: {node_with_score.score:.4f}")
    print(f"Text Snippet: {node_with_score.node.get_content()[:200]}...")
    print("-" * 30)

print('\n')

'''
What you asked and why you expected it to be hard
- 'What should I know?', and I expected it to ask me a follow up question'
What went wrong — wrong retrieval, missing information, the model guessed anyway?
- The model gave an answer anyway state the work hours, menu and so on.
When the retrieval failed, did the model's tone change — did it become less certain, or did it still sound confident even when it was wrong? What does this suggest about trusting AI-generated responses?
- It sounded confident and very expressive, it did not answer wrong, it just responded on what it knows. Ai generated response in this context are limited to the context it is operating in.
What you would change about the system to improve it
- I would add some suggested question for thing that are vague to provide more insight about the user query
'''

'''
The LlamaIndex lesson lists the steps that LlamaIndex automates: chunking, embedding, and indexing. How many lines of code did your LlamaIndex implementation take in your project? Compare that with the keyword RAG code from the Keyword-based RAG lesson, or with the code you would need to write each of those steps yourself. What does that tell you about the value of using a framework?
- I implemented less than 50 lines of code
- Framework hide all the abstraction code and make it easier to implement what is necessary or important with few lines of codes, making code readable and legible 

'''

'''
You have now built a system that answers questions from real documents. Describe a different use case — not a coffee shop — where this approach would add genuine value to a business or organization.
- if you are providing a service lets say a web hosting, thee are a lot of things that can be solved by getting the right document in-front of the user or information without the need to include an admin. Example: connecting a domain to your hosting, where to find a nameserver for your domain and so on.
'''

'''
What is one failure mode that RAG cannot fully prevent, even when retrieval is working correctly?
- It has to be hallucination, I notice the assistance always have an answer and never just admin that ' I dont know'.
- Such persistence can lead to always provide answer that maybe be misinform or misinterpret the retrieval information; combine it with incorrect prior knowledge and state information that isn't actually in the retrieved context
'''