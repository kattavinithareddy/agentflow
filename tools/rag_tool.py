from rag.retriever import get_retriever


retriever = get_retriever()


def retrieve_context(question: str) -> str:
    """
    Retrieve relevant documents from the AgentFlow knowledge base.
    """

    documents = retriever.invoke(question)

    if not documents:
        return "No relevant information was found in the knowledge base."

    context_parts = []

    for document in documents:
        context_parts.append(document.page_content)

    return "\n\n---\n\n".join(context_parts)