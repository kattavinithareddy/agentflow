#!/bin/sh

python -m rag.ingestion

exec uvicorn backend.main:app --host 0.0.0.0 --port 8000