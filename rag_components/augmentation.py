# augmentation.py
from langchain_core.prompts import PromptTemplate


def augment_query():
    prompt = PromptTemplate(
        template="""
      You are a helpful assistant that answers questions about YouTube videos.
Use the provided transcript as your primary source.
If the answer is not in the transcript, you may use your general knowledge
to answer, but clearly state that the answer is not from the video itself.

      {context}
      Question: {question}
    """,
        input_variables=['context', 'question']
    )
    return prompt
