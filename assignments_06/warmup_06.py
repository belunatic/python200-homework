from dotenv import load_dotenv
import os

if load_dotenv():
    print("API key loaded successfully.")
else:
    print("Warning: could not load API key. Check your .env file.")

# --- RAG Concepts --- 
# Concepts Q1

'''
Three teams at a software company are each building a different AI project. Add a comment block to your code that identifies the best approach — prompt engineering, fine-tuning, or RAG — for each scenario, and gives a 1-2 sentence explanation of your reasoning.

Scenario A: A legal team wants an assistant that can answer questions about their internal policy library — hundreds of PDFs that are updated every quarter.
- RAG will be ideal for this situation, here is why:
    - RAG can chunk the PDFs to small chunk for the model to perform keyword or semantic phrase search on the pdf's to retrieve the answers. The information retrieved will be from the law firm external data and not the internet improving the accuracy of the answer.

Scenario B: A startup wants their model to write product copy in a very specific brand voice — a dry, minimalist style that does not appear much online. They have 3,000 examples their in-house writers produced over the years.
- This scenario is best suited for Fine-tuning, here is why:
    -- Fine-tuning allows you to create a specific-style or pattern that the LLM can follow, especially with so many examples on hand, this will be the ideal approach.

Scenario C: A data analyst needs to ask an LLM questions about a single two-page report she just received. She does not need this to work for any other document.
- Prompt Engineering will be ideal for this, here is why:
    -- The process is back and forth conversation, no external data is needed but the context is required in order to for the LLM not to lose track of what the data analyst is asking and what it already relay to them.
'''

# Concepts Q2

'''
Why is a confidently wrong answer more harmful than one that says "I am not sure"? Give one example of a real situation where a confident hallucination could cause harm.
- Because such an answer create a string of wrong approach or answers; these answer can lead to more disaster or problem if not checked.
- Example:
    -- In the medical field, a user might input there symptoms to an LLM model and it might suggest them with prevention that may cause harm rather than good. So it would be ideal to just seek medical help from a professional.
'''

'''
Think about the tone of the response as well as its content — why does the way the model expresses an answer affect how much we trust it?
- The LLM tone sounds very confidence as you read it, I am sure even it was voices out it will still sounds confidence; Not like a humans, you can tell the confidence on their voice and since an LLM or machine do not have that capability of examine itself it lack that hesitation, making it very believable.
'''

# Concepts Q3

'''
Original List
steps = [
    "Generate a response from the LLM",
    "Extract text from source documents",
    "Receive the user's query",
    "Retrieve the most relevant chunks",
    "Convert text chunks into embeddings",
    "Inject retrieved chunks into the prompt",
    "Split text into chunks",
    "Embed the user's query",
]

Rearranged List with Description

step = [
"Receive the user's query", -> get the user query
"Embed the user's query", -> Cleaning the query, removing the stopword from the query
"Extract text from source documents", -> get the external data, then extra the text from each document
"Split text into chunks", -> breakdown the text into smaller chunks, so as to retrieve relevant chunks
"Convert text chunks into embeddings", -> chunks are scored to measure how relevant they are to the query that the user will pass on later.
"Inject retrieved chunks into the prompt", -> Get the most relevant chunk and add it to prompt as context for the LLM / Model
"Generate a response from the LLM", -> get the answer
]

'''

# Keyword RAG 

import string

def simple_keyword_retrieval(query, documents, verbose=True):
    """Keyword retrieval using token overlap scoring."""
    stopwords = {
        "a", "an", "the", "and", "or", "in", "on", "of", "for", "to", "is",
        "are", "was", "were", "by", "with", "at", "from", "that", "this",
        "as", "be", "it", "its", "their", "they", "we", "you", "our"
    }
    translator = str.maketrans("", "", string.punctuation)

    query_words = {
        w.translate(translator)
        for w in query.lower().split()
        if w not in stopwords
    }
    if verbose:
        print(f"\nQuery tokens (filtered): {sorted(query_words)}")

    scores = []
    for name, content in documents.items():
        content_words = {
            w.translate(translator)
            for w in content.lower().split()
            if w not in stopwords
        }
        overlap = query_words & content_words
        score = len(overlap)
        scores.append((score, name, content))
        if verbose:
            print(f"[{name}] overlap={score} -> {sorted(overlap)}")

    scores.sort(reverse=True)
    best = next(((name, content) for score, name, content in scores if score > 0), None)
    if best:
        if verbose:
            print(f"\nSelected best match: {best[0]}")
        return [best]
    else:
        if verbose:
            print("\nNo overlapping keywords found.")
        return [("None found", "No relevant content.")]

# RAG Q1

query = "What are your hours on weekends?"

documents = {
    "menu.txt": "We serve espresso, lattes, cappuccinos, and cold brew. Pastries include croissants and muffins baked fresh daily. Oat milk and almond milk are available.",
    "hours.txt": "We are open Monday through Friday from 7am to 7pm. On weekends we open at 8am and close at 5pm. We are closed on Thanksgiving and Christmas Day.",
    "hiring.txt": "We are currently hiring baristas and shift supervisors. Send your resume to jobs@groundworkcoffee.com.",
    "loyalty.txt": "Join our loyalty program to earn one point per dollar spent. Redeem 100 points for a free drink of your choice.",
}

answer = simple_keyword_retrieval(query, documents)
print(answer)

'''
explaining which document was selected and why.
- Since hours, hiring, and loyalty score the same, the result of score.sort(reverse=true) will sort the score tuple as follows:

    - First by score
    - If scores tie, by name
    - If names tie, by content

There for since score are the same the next thing it sorted by is alphabetic in reverse order, making loyalty a winning candidate.
'''

# RAG Q2
query = "Do you have anything without caffeine?"
answer = simple_keyword_retrieval(query, documents)
print('\n')
print('-'* 30)
print(answer)

'''
Which document was selected
- None
Whether keyword RAG got this right — and why or why not
- Keyword RAG got this one wrong, because the menu clearly express all the caffeine drinks it had and they were not detected by the model
What kind of retrieval would do better here
- Semantic phrase search RAG will be idea because it read the context and figure out the answer using the cosine similarity

'''

# RAG Q3

'''
Before running any code, predict which document will be selected for the query below. Write your prediction and your reasoning as a comment first, then run the code to check.
- The prediction will be "None Found" because no document contain any of the words from the query
'''

query = "How do I sign up for rewards?"
answer = simple_keyword_retrieval(query, documents)
print('\n')
print('-'* 30)
print(answer)

# Semantic RAG Concepts
'''
What is a vector embedding? (1-2 sentences)
- A list of floating-point numbers (an n-dimensional array) that translates unstructured data—such as text, images, audio, or video—into a numerical coordinate space

Two text chunks have cosine similarity scores of 0.85 and 0.30 with a given query. Which chunk is more relevant, and what does that number tell you about the relationship between the texts?
- The 0.85 text chunk is more relevant with the given query. The number tells us how similar two embeddings are to one another.

Why can semantic search find a relevant chunk even when none of the exact words from the query appear in the chunk?
- Using vector embedding and cosine similarity score, semantic search uses both to find the relationship between the query and data.

'''

# Q2
'''
| Feature                    | Keyword RAG                       | Semantic RAG |
|----------------------------|-----------------------------------|--------------|
| What is compared?          | Exact word overlap                | semantic similarity            |
| What is retrieved?         | Full document                     | Storage Context           |
| Can it handle synonyms?    | No                                | Yes          |
| Storage format             | Plain text dictionary             | Database            |
| Relevance score            | Number of overlapping keywords    | cosine Similarity            |

'''

#LlamaIndex

from llama_index.core import Settings,SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

# default LlamaIndex uses the older text-embedding-ada-002
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.llm = OpenAI(model="gpt-4o-mini")

# Load documents directly from PDFs in the folder
docs = SimpleDirectoryReader("./resources/brightleaf_pdfs").load_data()

# LlamaIndex provides a default storage index called VectorStoreIndex to store the chunked and embedded text from the documents
# Build a vector index automatically (handles chunking + embeddings)
index = VectorStoreIndex.from_documents(docs)

#query engine
#LlamaIndex uses a helper object called a "query engine" that wraps the entire context retrieval, augmentation, and response generation process.
query_engine = index.as_query_engine(similarity_top_k=3)

# query
questions = [
    "What employee benefits does BrightLeaf offer?",
    "What are BrightLeaf's security policies?",
]

for q in questions:
    print(f"\nQ: {q}")
    response = query_engine.query(q)
    print("A:", response)
    
    for node_with_score in response.source_nodes:
        print(f"Node ID: {node_with_score.node.node_id}")
        print(f"Similarity Score: {node_with_score.score:.4f}")
        print(f"Text Snippet: {node_with_score.node.get_content()[:150]}...")
        print("-" * 30)

    print('\n')

'''
Do the retrieved chunks look relevant to the question?
- Yes
Does the model's response sound confident and specific, or does it hedge with phrases like "based on the context" or "I'm not sure"? Note what you observe about the tone.
- It sounded confidence and specific, retrieving relevant information from all documents related to the context
Did anything unexpected get retrieved?
- Not I could see.
'''

# Q2
query_engine_1 = index.as_query_engine(similarity_top_k=1)
query_engine_5 = index.as_query_engine(similarity_top_k=5)

print('\nsimilarity_top_k=1','*' * 30, '\n')
print(f"\nQ: {questions[0]}")
response = query_engine_1.query(questions[0])
print("A:", response)

for node_with_score in response.source_nodes:
    print(f"Node ID: {node_with_score.node.node_id}")
    print(f"Similarity Score: {node_with_score.score:.4f}")
    print(f"Text Snippet: {node_with_score.node.get_content()[:150]}...")
    print("-" * 30)

print('\nsimilarity_top_k=5','*' * 30, '\n')
print(f"\nQ: {questions[0]}")
response = query_engine_5.query(questions[0])
print("A:", response)

for node_with_score in response.source_nodes:
    print(f"Node ID: {node_with_score.node.node_id}")
    print(f"Similarity Score: {node_with_score.score:.4f}")
    print(f"Text Snippet: {node_with_score.node.get_content()[:150]}...")
    print("-" * 30)

'''
explaining how the response changed (if at all) and whether more retrieved context is always better?
- the response changed from being serious and to the point to being more casual and informative. The more chunk you get the more it turn to be more casual return rather than be a robotic. So more is better.
'''

# Q3

print('\nStruggle Question','*' * 30, '\n')
print(f"\nQ: {questions[0]}")
response = query_engine.query('What happen when someone dies on the company properties?')
print("A:", response)

for node_with_score in response.source_nodes:
    print(f"Node ID: {node_with_score.node.node_id}")
    print(f"Similarity Score: {node_with_score.score:.4f}")
    print(f"Text Snippet: {node_with_score.node.get_content()[:150]}...")
    print("-" * 30)

'''
explaining what you expected, what actually happened, and what you would change about the system to handle this kind of query better.
- As expected, the model wont have a concrete answer to this, but it refer me to company incident report or emergency protocols which was good answer and right direction.
- I would change the system by adding to the PDFs addition information can be reached at '...', this way the LLM can refere to it if it fails to answer or not sure about the answer, making it robust to handle the undocumented.
'''

# Q4

Settings.llm = OpenAI(model="gpt-4o")

from llama_index.llms.openai import OpenAI
from llama_index.core.evaluation import FaithfulnessEvaluator, RelevancyEvaluator

# Create Judge LLM
llm = OpenAI(model="gpt-4o-mini", temperature=0.2)

# Define evaluator
faithfulness_evaluator = FaithfulnessEvaluator(llm=llm)
relevancy_evaluator = RelevancyEvaluator(llm=llm)

# Get response to query
q = "What employee benefits does BrightLeaf offer?"
response = query_engine.query(q)

print('\n', '*'*30)
# Evaluate faithfulness and relevancy
faithfulness_result = faithfulness_evaluator.evaluate_response(query=q, response=response)
print("Faithfulness Evaluation: " + str(faithfulness_result.score))

relevancy_result = relevancy_evaluator.evaluate_response(query=q, response=response)
print("Relevancy Result: " + str(relevancy_result.score))

# Get response to an expected query
q = "What food is served in the company cafeteria?"
response = query_engine.query(q)

print('\n', '*'*30)
# Evaluate faithfulness and relevancy
faithfulness_result = faithfulness_evaluator.evaluate_response(query=q, response=response)
print("Faithfulness Evaluation: " + str(faithfulness_result.score))

relevancy_result = relevancy_evaluator.evaluate_response(query=q, response=response)
print("Relevancy Result: " + str(relevancy_result.score))

'''
What does a faithfulness score of 1.0 mean? What would a score of 0.0 indicate?
- 1.0 mean the response is not lying or hallucinating, while 0.0 mean it is.
What does a relevancy score measure, and how is it different from faithfulness?
- Relevancy score measure how relevance the response is to the query, while the faithful measure if the response is true or not
Did the scores change between your two queries? If so, why do you think that happened?
- Yes, I think what happen was that the model could not find the answer to the query but gave an answer anyway, and that answer is not relevant to the query.
What is the "LLM-as-a-judge" approach, and why is it used for RAG evaluation instead of a simple accuracy metric?
- because we are judging a Natural Language that can not be easily measured, therefore we use another LLM-as-a-judge; also add another layer of reducing the human involvement in every evaluation of the RAG system.


'''