from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from langchain_openai import ChatOpenAI, OpenAI
import os

app = FastAPI()
openai_api_key=os.getenv("OPENAI_API_KEY")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chatopenai-streaming-endpoint")
async def main():
    response_text = ""

    # OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=512)
    # llm = OpenAI(model="gpt-4o", temperature=0, max_tokens=512)

    model = ChatOpenAI(openai_api_key= openai_api_key, model="gpt-4o", temperature=0, streaming=True,)
    messages =[("Tell me a joke about cat")]

    chunks = []
    async def event_stream():
        async for chunk in model.astream(messages):
            chunks.append(chunk)
            yield f"data: {chunk.content}\n\n"
 
    return StreamingResponse(event_stream(), media_type="text/event-stream")
