from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

from langchain_openai import ChatOpenAI, OpenAI, AzureChatOpenAI

import os
import time

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
    start_time = time.time()  # Start timing

    # OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=512)
    response_text = ""
    llm = AzureChatOpenAI(
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION_CHAT"),
        azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )
    messages =[("Write me a song about sparkling water.")]

    async def event_stream():
        for chunk in llm.stream(messages):
            yield f"data: {chunk}\n\n"
            
    response = StreamingResponse(event_stream(), media_type="text/event-stream")

    end_time = time.time()  # End timing
    time_taken = end_time - start_time  # Time taken
    print(f"Time taken to generate response: {time_taken} seconds")

    return response