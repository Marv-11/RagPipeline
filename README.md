# RagPipeline

A minimal FastAPI service for running a Retrieval-Augmented Generation (RAG) pipeline.

## Requirements
- Python 3.8 or later

## Setup
1. Create and activate a virtual environment (optional if you rely on Poetry's venv).
2. Install dependencies with Poetry:
```bash
poetry install
```
3. Configure environment variables (see below).

## Environment Variables
Copy the example file and edit it:
```bash
cp .env.example .env
```

## Run the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## Project Structure
- `main.py` - FastAPI app entrypoint
- `assets/` - Supporting files

## Notes
If you change the server port or host in your environment, update the `uvicorn` command accordingly.
