from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


load_dotenv()


DOCUMENTS_DIR = Path(__file__).parent / "documents"
CHROMA_DIR = Path(__file__).parent / "chroma_db"


def ingest_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )
        documents.extend(loader.load())

    if not documents:
        raise ValueError("No documents found in rag/documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vector_store = Chroma(
        collection_name="agentflow_knowledge",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    existing_ids = vector_store.get()["ids"]

    if existing_ids:
        vector_store.delete(ids=existing_ids)

    vector_store.add_documents(chunks)

    print(f"Loaded documents: {len(documents)}")
    print(f"Created chunks: {len(chunks)}")
    print("ChromaDB collection refreshed successfully.")


if __name__ == "__main__":
    ingest_documents()