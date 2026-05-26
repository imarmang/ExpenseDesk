import logging
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

app = FastAPI(
    title="ExpenseDesk API",
    description="AI-powered expense assistant backend",
    version="0.1.0"
)

# Ollama client
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://localhost:30000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model (DTO)
class ChatRequest(BaseModel):
    message: str

# Routes
# Status check
@app.get( "/" )
async def root():
    return { "status": "ExpenseDesk API is running" }

@app.post( "/chat" )
async def chat( request: ChatRequest ):
    log.info( "──────────────────────────────────────" )
    log.info( f"incoming message: {request.message}" )

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": """You are a SQL expert for a company expense management system.
    The database tracks employee expenses, approvals, departments, vendors and categories.

    Use your available tools to:
    1. Call list_tables to discover what tables exist
    2. Call get_schema on relevant tables to get column names
    3. Generate and execute a SELECT query to answer the question

    Rules:
    - Only use SELECT statements
    - No explanation, no markdown, no code blocks
    - Use only tables and columns you discover via tools"""
        },
        {
            "role": "user",
            "content": request.message
        }
    ]

    log.info(f"sending request to Ollama → model: qwen2.5-coder:7b")
    start = time.time()


    response = ollama_client.chat.completions.create(
        model="qwen2.5-coder:7b",
        messages=messages,
        temperature=0,
    )

    elapsed = round( time.time() - start, 2 )
    log.info( f"Ollama responded in {elapsed}s" )

    sql = response.choices[0].message.content.strip()
    log.info( f"generated SQL: {sql}" )
    log.info( f"tokens used: {response.usage.total_tokens}" )
    log.info( "──────────────────────────────────────" )

    return {
        "response": "Here is the query I generated for you.",
        "sql": sql,
    }
