from typing import Literal, TypedDict
import asyncio
import os

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from tools.rag_tool import retrieve_context
from tools.web_tool import web_search


load_dotenv()


class AgentState(TypedDict):
    question: str
    route: str
    context: str
    answer: str


class RouteDecision(BaseModel):
    route: Literal["rag", "web", "mcp", "direct"]


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)


router_llm = llm.with_structured_output(RouteDecision)


def router_node(state: AgentState):

    question = state["question"]

    prompt = f"""
You are the routing agent for AgentFlow.

Choose exactly one route:

rag
Use this when the question is about information contained
in the private AgentFlow knowledge base.

web
Use this when the question requires current, recent,
external, or internet-based information.

mcp
Use this when the user asks you to perform a calculation
or mathematical operation using the MCP calculator tool.

direct
Use this for general knowledge, programming concepts,
explanations, or reasoning.

User question:
{question}
"""

    decision = router_llm.invoke(prompt)

    return {
        "route": decision.route
    }


def retrieve_node(state: AgentState):

    context = retrieve_context(
        state["question"]
    )

    return {
        "context": context
    }


def web_search_node(state: AgentState):

    context = web_search(
        state["question"]
    )

    return {
        "context": context
    }


async def call_mcp_calculator(
    expression: str
) -> str:

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/server.py"],
    )

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                "calculate",
                {
                    "expression": expression
                },
            )

            if result.content:

                first_item = result.content[0]

                if hasattr(
                    first_item,
                    "text"
                ):
                    return first_item.text

                return str(first_item)

            return (
                "No result returned by MCP calculator."
            )


def extract_expression(
    question: str
) -> str:

    expression = question.lower()

    prefixes = [
        "calculate",
        "what is",
        "compute",
        "solve",
    ]

    for prefix in prefixes:

        expression = expression.replace(
            prefix,
            ""
        )

    return expression.strip()


def mcp_node(state: AgentState):

    question = state["question"]

    expression = extract_expression(
        question
    )

    result = asyncio.run(
        call_mcp_calculator(
            expression
        )
    )

    return {
        "context": (
            f"MCP Calculator Result: {result}"
        )
    }


def direct_answer_node(state: AgentState):

    response = llm.invoke(
        f"""
You are AgentFlow, an AI engineering assistant.

Answer the user's question clearly and accurately.

User question:
{state["question"]}
"""
    )

    return {
        "answer": response.content
    }


def answer_node(state: AgentState):

    question = state["question"]
    context = state["context"]
    route = state["route"]


    if route == "rag":

        source_description = """
The context comes from the private AgentFlow knowledge base.
Use it as the source of truth.
"""


    elif route == "web":

        source_description = """
The context comes from web search results.
Use the retrieved information to answer the question.
"""


    elif route == "mcp":

        source_description = """
The context comes from the MCP calculator tool.
Use the calculator result directly.
"""


    else:

        source_description = """
This is a general knowledge question.
"""


    prompt = f"""
You are AgentFlow, an AI engineering assistant.

Route:
{route}

{source_description}

Retrieved context:
{context}

User question:
{question}

Instructions:
- Give a clear and useful answer.
- For RAG questions, do not invent facts outside the retrieved context.
- For web questions, base the answer on the retrieved web information.
- For MCP questions, use the calculator result.
- If retrieved information is insufficient, clearly say so.
- For direct questions, answer normally.
"""


    response = llm.invoke(
        prompt
    )

    return {
        "answer": response.content
    }


def route_question(
    state: AgentState
):

    return state["route"]


graph_builder = StateGraph(
    AgentState
)


graph_builder.add_node(
    "router",
    router_node
)

graph_builder.add_node(
    "retrieve",
    retrieve_node
)

graph_builder.add_node(
    "web_search",
    web_search_node
)

graph_builder.add_node(
    "mcp",
    mcp_node
)

graph_builder.add_node(
    "direct_answer",
    direct_answer_node
)

graph_builder.add_node(
    "answer",
    answer_node
)


graph_builder.add_edge(
    START,
    "router"
)


graph_builder.add_conditional_edges(
    "router",
    route_question,
    {
        "rag": "retrieve",
        "web": "web_search",
        "mcp": "mcp",
        "direct": "direct_answer",
    },
)


graph_builder.add_edge(
    "retrieve",
    "answer"
)

graph_builder.add_edge(
    "web_search",
    "answer"
)

graph_builder.add_edge(
    "mcp",
    "answer"
)

graph_builder.add_edge(
    "direct_answer",
    END
)

graph_builder.add_edge(
    "answer",
    END
)


graph = graph_builder.compile()