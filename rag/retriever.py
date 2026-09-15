from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

CHROMA_DIR = Path(__file__).parent / "chroma_db"


def get_retriever():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vector_store = Chroma(
        collection_name="agentflow_knowledge",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )