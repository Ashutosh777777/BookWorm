# # ---- Cell ----
# import os
# import glob
# import tiktoken
# import numpy as np
# from dotenv import load_dotenv
# from langchain_openai import OpenAIEmbeddings
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.document_loaders import DirectoryLoader, TextLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from sklearn.manifold import TSNE
# import plotly.graph_objects as go

# # ---- Cell ----
# MODEL = "llama3.2"
# db_name = "vector_db"
# load_dotenv(override=True)

# # ---- Cell ----
# knowledge_base_path = "books/book.pdf"
# files = glob.glob(knowledge_base_path) # glob finds files whose names match a specified pattern.
# print(f"found {len(files)} files in the knowledge base")
# entire_knowledge_base = ""

# from pypdf import PdfReader
# # for file_path in files:
# #     with open(file_path, 'r', encoding='utf-8')

# for file_path in files:
#     reader = PdfReader(file_path)
#     for page in reader.pages:
#         text = page.extract_text()
#         if text:
#             entire_knowledge_base += text
#             entire_knowledge_base += "\n\n"

# print(f"Total characters in knowledge base: {len(entire_knowledge_base):,}")

# # ---- Cell ----
# import tiktoken
# encoding = tiktoken.get_encoding('cl100k_base')
# tokens = encoding.encode(entire_knowledge_base)

# print(f"Token length {len(tokens)}")

# # ---- Cell ----
# from langchain_community.document_loaders import DirectoryLoader
# from langchain_community.document_loaders import PyPDFLoader

# loader = DirectoryLoader(
#     "knowledge-base",
#     glob="**/*.pdf",
#     loader_cls=PyPDFLoader
# )

# documents = loader.load()

# print(f"Loaded {len(documents)} documents")

# # ---- Cell ----
# documents[1]

# # ---- Cell ----
# text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
# chunks = text_splitter.split_documents(documents)

# print(f"Divided into {len(chunks)} chunks")
# print(f"First chunk is \n\n{chunks[0]}")

# # ---- Cell ----
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# if os.path.exists(db_name):
#     Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection
# vectorstore = Chroma.from_documents(documents=chunks, embedding = embeddings, persist_directory=db_name)
# print(f"Vectorstore create with {vectorstore._collection.count()} documents")

# # ---- Cell ----
# collection = vectorstore._collection
# count = collection.count()

# sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
# dimensions = len(sample_embedding)
# print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")


# # ---- Cell ----
# # # Prework

# # result = collection.get(include=['embeddings', 'documents', 'metadatas'])
# # vectors = np.array(result['embeddings'])
# # documents = result['documents']
# # metadatas = result['metadatas']
# # doc_types = [metadata.get('doc_type', 'unknown') for metadata in metadatas]
# # colors = [['blue', 'green', 'red', 'orange'][['products', 'employees', 'contracts', 'company'].index(t)] for t in doc_types]

# # ---- Cell ----
# # Prework

# result = collection.get(include=['embeddings', 'documents', 'metadatas'])

# vectors = np.array(result['embeddings'])
# documents = result['documents']
# metadatas = result['metadatas']

# doc_types = [metadata.get('doc_type', 'unknown') for metadata in metadatas]

# color_map = {
#     'chapters': 'blue',
#     'bugs': 'green',
#     'takeaways': 'red',
#     'summary': 'orange'
# }

# colors = [color_map.get(t, 'gray') for t in doc_types]

# # ---- Cell ----
# # We humans find it easier to visalize things in 2D!
# # Reduce the dimensionality of the vectors to 2D using t-SNE
# # (t-distributed stochastic neighbor embedding)
# tsne = TSNE(n_components=2, random_state=42)
# reduced_vectors = tsne.fit_transform(vectors)

# # Create the 2D scatter plot
# fig = go.Figure(data=[go.Scatter(
#     x=reduced_vectors[:, 0],
#     y=reduced_vectors[:, 1],
#     mode='markers',
#     marker=dict(size=5, color=colors, opacity=0.8),
#     text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
#     hoverinfo='text'
# )])

# fig.update_layout(title='2D Chroma Vector Store Visualization',
#     scene=dict(xaxis_title='x',yaxis_title='y'),
#     width=800,
#     height=600,
#     margin=dict(r=20, b=10, l=10, t=40)
# )

# fig.show()

# # ---- Cell ----
# # 3D huh?

# tsne = TSNE(n_components=3, random_state=42)
# reduced_vectors = tsne.fit_transform(vectors)

# # Create the 3D scatter plot
# fig = go.Figure(data=[go.Scatter3d(
#     x=reduced_vectors[:, 0],
#     y=reduced_vectors[:, 1],
#     z=reduced_vectors[:, 2],
#     mode='markers',
#     marker=dict(size=5, color=colors, opacity=0.8),
#     text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
#     hoverinfo='text'
# )])

# fig.update_layout(
#     title='3D Chroma Vector Store Visualization',
#     scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='z'),
#     width=900,
#     height=700,
#     margin=dict(r=10, b=10, l=10, t=40)
# )

# fig.show()

# # ---- Cell ----
# from dotenv import load_dotenv
# from langchain_ollama import ChatOllama

# from langchain_chroma import Chroma
# from langchain_core.messages import SystemMessage, HumanMessage
# from langchain_huggingface import HuggingFaceEmbeddings
# import gradio as gr

# # ---- Cell ----
# MODEL = "llama3.2"
# DB_NAME = "vector_db"
# load_dotenv(override=True)

# # ---- Cell ----
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)

# # ---- Cell ----
# retreiver = vectorstore.as_retriever()
# llm = ChatOllama(temperature=0, model=MODEL)

# # ---- Cell ----
# retreiver.invoke("What is HTTP?")

# # ---- Cell ----
# llm.invoke("What is HTTP?")

# # ---- Cell ----
# SYSTEM_PROMPT_TEMPLATE = """
# You are a knowledgeable, friendly assistant that helps the user with bug hunting in cyber security.
# You are chatting with a user about Hacking.
# If relevant, use the given context to answer any question.
# If you don't know the answer, say so.
# Context:
# {context}
# """

# # ---- Cell ----
# def answer_question(question: str, history):
#     docs = retreiver.invoke(question)
#     context = "\n\n".join(doc.page_content for doc in docs)
#     system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context = context)
#     response = llm.invoke([SystemMessage(content = system_prompt), HumanMessage(content=question)])
#     return response.content

# # ---- Cell ----
# answer_question("What is HTTP PARAMETER POLLUTION?", [])

# # ---- Cell ----

# NETWORKING_SYSTEM_PROMPT = """
# You are a specialist in networking concepts relevant to web security and bug hunting.
# Focus on: HTTP/HTTPS, TCP/IP, DNS, ports, request/response cycles, headers,
# status codes, cookies, redirects, CORS, and network-level attack surfaces.
# Use the provided context to answer. If the question is outside networking, say so.
 
# Context:
# {context}
# """
 
# SECURITY_SYSTEM_PROMPT = """
# You are a specialist in web application security and vulnerability hunting.
# Focus on: XSS, SQLi, CSRF, SSRF, RCE, XXE, IDOR, OAuth flaws, subdomain takeovers,
# race conditions, template injection, memory vulnerabilities, and bug bounty methodology.
# Use the provided context to answer. If the question is outside security, say so.
 
# Context:
# {context}
# """
 
 

# # ---- Cell ----

# import json
 
# def classify_query(query: str) -> str:
#     """Returns 'networking', 'security', or 'both'."""
#     prompt = f"""Classify the following query into exactly one of these categories:
# - networking  (HTTP, DNS, TCP/IP, ports, headers, cookies, redirects)
# - security    (XSS, SQLi, CSRF, vulnerabilities, exploits, bug bounty)
# - both        (query spans both networking and security topics)
 
# Respond with ONLY a JSON object like: {{"domain": "networking"}}
 
# Query: {query}"""
 
#     result = llm.invoke([HumanMessage(content=prompt)])
#     try:
#         parsed = json.loads(result.content.strip())
#         domain = parsed.get("domain", "both").lower()
#         if domain not in ("networking", "security", "both"):
#             domain = "both"
#         return domain
#     except Exception:
#         return "both"  # safe fallback
 
 
# def networking_agent(query: str) -> str:
#     docs = retreiver.invoke(query)
#     context = "\n\n".join(doc.page_content for doc in docs)
#     system_prompt = NETWORKING_SYSTEM_PROMPT.format(context=context)
#     response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=query)])
#     return response.content
 
 
# def security_agent(query: str) -> str:
#     docs = retreiver.invoke(query)
#     context = "\n\n".join(doc.page_content for doc in docs)
#     system_prompt = SECURITY_SYSTEM_PROMPT.format(context=context)
#     response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=query)])
#     return response.content
 
 

# # ---- Cell ----

# def coordinator_agent(query: str, history) -> str:
#     """
#     Coordinator-based multi-agent RAG architecture.
#     Classifies the query and delegates to domain-specialized agents.
#     For cross-domain queries, both agents respond and are synthesized.
#     """
#     domain = classify_query(query)
 
#     if domain == "networking":
#         return networking_agent(query)
 
#     elif domain == "security":
#         return security_agent(query)
 
#     else:  # both — multi-agent collaboration
#         net_answer = networking_agent(query)
#         sec_answer = security_agent(query)
 
#         synthesis_prompt = f"""Two specialized agents have answered the following query.
# Synthesize their answers into one clear, coherent response.
 
# Query: {query}
 
# Networking Agent Answer:
# {net_answer}
 
# Security Agent Answer:
# {sec_answer}
 
# Provide a unified, well-structured response:"""
 
#         final = llm.invoke([
#             SystemMessage(content="You are a coordinator that synthesizes expert answers into clear responses."),
#             HumanMessage(content=synthesis_prompt)
#         ])
#         return final.content
 

# # ---- Cell ----
# gr.ChatInterface(coordinator_agent, title="Bug Hunting Assistant (Multi-Agent)").launch()

# # ---- Cell ----


import os
import json

from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_huggingface import HuggingFaceEmbeddings
import gradio as gr

# ── Config ────────────────────────────────────────────────────────────────────
MODEL   = "llama3.2"
DB_NAME = "vector_db"

# Ollama host: use env var so Docker can override it
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# ── Setup ─────────────────────────────────────────────────────────────────────
embeddings  = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)
retriever   = vectorstore.as_retriever()
llm         = ChatOllama(temperature=0, model=MODEL, base_url=OLLAMA_HOST)

# ── System prompts ────────────────────────────────────────────────────────────
NETWORKING_SYSTEM_PROMPT = """
You are a specialist in networking concepts relevant to web security and bug hunting.
Focus on: HTTP/HTTPS, TCP/IP, DNS, ports, request/response cycles, headers,
status codes, cookies, redirects, CORS, and network-level attack surfaces.
Use the provided context to answer. If the question is outside networking, say so.

Context:
{context}
"""

SECURITY_SYSTEM_PROMPT = """
You are a specialist in web application security and vulnerability hunting.
Focus on: XSS, SQLi, CSRF, SSRF, RCE, XXE, IDOR, OAuth flaws, subdomain takeovers,
race conditions, template injection, memory vulnerabilities, and bug bounty methodology.
Use the provided context to answer. If the question is outside security, say so.

Context:
{context}
"""

# ── Agents ────────────────────────────────────────────────────────────────────
def classify_query(query: str) -> str:
    prompt = f"""Classify the following query into exactly one of these categories:
- networking  (HTTP, DNS, TCP/IP, ports, headers, cookies, redirects)
- security    (XSS, SQLi, CSRF, vulnerabilities, exploits, bug bounty)
- both        (query spans both networking and security topics)

Respond with ONLY a JSON object like: {{"domain": "networking"}}

Query: {query}"""

    result = llm.invoke([HumanMessage(content=prompt)])
    try:
        parsed = json.loads(result.content.strip())
        domain = parsed.get("domain", "both").lower()
        return domain if domain in ("networking", "security", "both") else "both"
    except Exception:
        return "both"


def networking_agent(query: str) -> str:
    docs    = retriever.invoke(query)
    context = "\n\n".join(doc.page_content for doc in docs)
    prompt  = NETWORKING_SYSTEM_PROMPT.format(context=context)
    return llm.invoke([SystemMessage(content=prompt), HumanMessage(content=query)]).content


def security_agent(query: str) -> str:
    docs    = retriever.invoke(query)
    context = "\n\n".join(doc.page_content for doc in docs)
    prompt  = SECURITY_SYSTEM_PROMPT.format(context=context)
    return llm.invoke([SystemMessage(content=prompt), HumanMessage(content=query)]).content


def coordinator_agent(query: str, history) -> str:
    domain = classify_query(query)

    if domain == "networking":
        return networking_agent(query)

    elif domain == "security":
        return security_agent(query)

    else:  # both — multi-agent collaboration
        net_answer = networking_agent(query)
        sec_answer = security_agent(query)

        synthesis_prompt = f"""Two specialized agents have answered the following query.
Synthesize their answers into one clear, coherent response.

Query: {query}

Networking Agent Answer:
{net_answer}

Security Agent Answer:
{sec_answer}

Provide a unified, well-structured response:"""

        return llm.invoke([
            SystemMessage(content="You are a coordinator that synthesizes expert answers into clear responses."),
            HumanMessage(content=synthesis_prompt)
        ]).content


# ── Launch ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    gr.ChatInterface(
        coordinator_agent,
        title="Bug Hunting Assistant (Multi-Agent)"
    ).launch(server_name="0.0.0.0", server_port=7860)