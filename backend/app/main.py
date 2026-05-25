from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="ExpenseDesk API",
    description="AI-powered expense assistant backend",
    version="0.1.0",
)

# CORS (Cross-origin resource sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest( BaseModel ):
    message: str

# Routes
@app.get( "/chat" )
async def root():
    return { "status": "ExpenseDesk API is running" }

@app.post( "/chat" )
async def chat( request: ChatRequest ):
    return { "response": f"Received: {request.message}",
             "sql": "SELECT * FROM expenses LIMIT 10;",
    }
