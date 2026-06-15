import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()


def embedding_function(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model='models/gemini-embedding-2',
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 8})
    return retriever
