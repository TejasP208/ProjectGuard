from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from axiom_ai import Chatbot_stream
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Streaming response
@app.get("/chat-stream")
def chat_stream(prompt: str):
    return StreamingResponse(Chatbot_stream(prompt), media_type="text/plain")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)