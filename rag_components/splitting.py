from langchain_text_splitters import RecursiveCharacterTextSplitter


def splitter(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=200)
    chunks = text_splitter.create_documents([text])
    return chunks
