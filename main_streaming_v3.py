from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

from langchain_openai import ChatOpenAI, OpenAI, AzureChatOpenAI

import os

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

@app.get("/azureopenai-streaming-endpoint")
async def main():

    # OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=512)
    response_text = ""
    llm = AzureChatOpenAI(
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION_CHAT"),
        azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )
    messages =[("Tell me a joke about dogs")]

    async def event_stream():
        for chunk in llm.stream(messages):
            yield f"data: {chunk}\n\n"
            
    return StreamingResponse(event_stream(), media_type="text/event-stream")