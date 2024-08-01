from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

from langchain_openai import OpenAI

app = FastAPI()
client = AsyncOpenAI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/main-streaming-endpoint")
async def main():
    response_text = ""
    llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=512)

    async def event_stream():
        for chunk in llm.stream("Write me a song about sparkling water."):
            yield f"data: {chunk}\n\n"
            
    return StreamingResponse(event_stream(), media_type="text/event-stream")
