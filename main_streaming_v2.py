from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

from langchain_openai import ChatOpenAI, OpenAI

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

@app.get("/chatopenai-streaming-endpoint")
async def main():
    response_text = ""

    # OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=512)
    # llm = OpenAI(model="gpt-4o", temperature=0, max_tokens=512)

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    messages =[("Tell me a joke about dogs")]


    async def event_stream():
        for chunk in llm.stream(messages):
            yield f"data: {chunk.content}\n\n"
 
    return StreamingResponse(event_stream(), media_type="text/event-stream")
