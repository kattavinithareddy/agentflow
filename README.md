\# AgentFlow



> AI Engineering Assistant built with LangGraph, RAG, MCP tools, web search, FastAPI, and Gemini.



AgentFlow is an AI engineering assistant that intelligently routes user questions to the most appropriate capability:



\- 🔍 \*\*RAG\*\* — retrieves information from a private knowledge base

\- 🌐 \*\*Web Search\*\* — retrieves current external information

\- ⚙️ \*\*MCP Calculator\*\* — performs mathematical calculations through an MCP tool

\- ✨ \*\*Direct Reasoning\*\* — handles general programming, technical, and reasoning questions



The project demonstrates practical AI engineering concepts including agent orchestration, retrieval-augmented generation, tool integration, API development, testing, and Dockerization.



\---



\## Architecture



```text

&#x20;                        ┌──────────────────────┐

&#x20;                        │      User Query      │

&#x20;                        └──────────┬───────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌──────────────────────┐

&#x20;                        │   LangGraph Router   │

&#x20;                        └──────────┬───────────┘

&#x20;                                   │

&#x20;             ┌─────────────────────┼─────────────────────┐

&#x20;             │                     │                     │

&#x20;             ▼                     ▼                     ▼

&#x20;       ┌───────────┐         ┌───────────┐        ┌───────────┐

&#x20;       │    RAG    │         │    Web    │        │    MCP    │

&#x20;       │ Knowledge │         │  Search   │        │ Calculator│

&#x20;       └─────┬─────┘         └─────┬─────┘        └─────┬─────┘

&#x20;             │                     │                     │

&#x20;             └─────────────────────┼─────────────────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌──────────────────────┐

&#x20;                        │    Answer Generator  │

&#x20;                        │       Gemini         │

&#x20;                        └──────────┬───────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌──────────────────────┐

&#x20;                        │     FastAPI API      │

&#x20;                        └──────────┬───────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌──────────────────────┐

&#x20;                        │    Web Frontend      │

&#x20;                        └──────────────────────┘

