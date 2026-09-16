# AgentFlow

AI Engineering Assistant built with LangGraph, RAG, MCP, FastAPI, Docker, and Google Gemini.

AgentFlow is a multi-route AI assistant that intelligently decides how to handle a user's question. Depending on the request, it can use a private knowledge base with RAG, perform web search, call an MCP calculator tool, or answer directly using an LLM.

## 🚀 Live Demo

https://agentflow-uwon.onrender.com

## ✨ Features

- Intelligent query routing using LangGraph
- Retrieval-Augmented Generation (RAG)
- ChromaDB vector database
- Gemini Embedding 001 for document embeddings
- Web search using Tavily
- MCP-based calculator tool
- Direct LLM reasoning
- FastAPI backend
- Dockerized application
- Deployed on Render
- Browser-based chat interface

## 🏗️ Architecture

```text
                         User
                          │
                          ▼
                  AgentFlow Frontend
                          │
                          ▼
                    FastAPI /chat
                          │
                          ▼
                    LangGraph Router
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
        ▼                 ▼                  ▼
       RAG              Web Search           MCP
        │                 │                  │
        ▼                 ▼                  ▼
   ChromaDB             Tavily         Calculator Tool
        │                 │                  │
        └─────────────────┴──────────────────┘
                          │
                          ▼
                    Gemini LLM
                          │
                          ▼
                    Final Answer