from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agents.graph import graph


BASE_DIR = Path(__file__).parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI(
    title="AgentFlow",
    description="AI Engineering Assistant using LangGraph, RAG and MCP",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Question to send to AgentFlow"
    )


class ChatResponse(BaseModel):
    answer: str
    route: str


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


@app.get("/")
def serve_frontend():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AgentFlow"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    try:
        print(f"Received question: {request.question}")

        result = graph.invoke({
            "question": request.question.strip(),
            "route": "",
            "context": "",
            "answer": ""
        })

        print(f"Graph completed. Route: {result.get('route')}")

        answer = result.get("answer", "")

        # Gemini may return structured content blocks.
        if isinstance(answer, list):
            text_parts = []

            for item in answer:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        text_parts.append(
                            item.get("text", "")
                        )

            answer = "\n".join(text_parts)

        # Safety fallback for other structured response formats.
        if not isinstance(answer, str):
            answer = str(answer)

        answer = answer.strip()

        print(f"Final answer: {answer}")

        if not answer:
            raise HTTPException(
                status_code=500,
                detail="AgentFlow returned an empty response."
            )

        return {
            "answer": answer,
            "route": result.get(
                "route",
                "unknown"
            )
        }

    except HTTPException:
        raise

    except Exception as error:

        print(
            f"AgentFlow error: {type(error).__name__}: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "AgentFlow could not process "
                "your request. Please try again."
            )
        )