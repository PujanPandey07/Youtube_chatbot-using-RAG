from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from .splitting import splitter
from .augmentation import augment_query
from .embeddingsandvectorstore import embedding_function
from .transcript import get_transcript, extract_video_id
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# In-memory cache: { video_id: retriever }
_retriever_cache = {}


def format_docs(retrieved_docs):
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    return context_text


def build_retriever(url):
    video_id = extract_video_id(url)

    if video_id in _retriever_cache:
        print(f"[Cache HIT] Retriever for video_id: {video_id}")
        return _retriever_cache[video_id]

    print(f"[Cache MISS] Building retriever for video_id: {video_id}")
    transcript = get_transcript(video_id)
    chunks = splitter(transcript)
    retriever = embedding_function(chunks)

    _retriever_cache[video_id] = retriever
    return retriever


def create_chain(retriever):
    prompt = augment_query()

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    parser = StrOutputParser()

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    return parallel_chain | prompt | llm | parser
