from agents.graph import graph


def run_agent(question: str):
    result = graph.invoke({
        "question": question,
        "route": "",
        "context": "",
        "answer": "",
    })

    answer = result["answer"]

    if isinstance(answer, list):
        text_parts = []

        for item in answer:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))

        result["answer"] = "\n".join(text_parts)

    return result


def test_rag_route():
    result = run_agent(
        "What vector database does AgentFlow use?"
    )

    assert result["route"] == "rag"
    assert "ChromaDB" in result["answer"]


def test_direct_route():
    result = run_agent(
        "Explain binary search in simple terms"
    )

    assert result["route"] == "direct"
    assert result["answer"]


def test_web_route():
    result = run_agent(
        "What are the latest developments in AI agents?"
    )

    assert result["route"] == "web"
    assert result["answer"]


def test_mcp_route():
    result = run_agent(
        "Calculate 25 * 4 + 10"
    )

    assert result["route"] == "mcp"
    assert "110" in result["answer"]