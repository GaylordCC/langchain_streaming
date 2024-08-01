from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

from langchain_openai import ChatOpenAI, OpenAI

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

@app.get("/main-streaming-endpoint")
async def main():
    start_time = time.time()  # Start timing

    # OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=512)
    response_text = ""
    llm = ChatOpenAI(model="gpt-4", temperature=0, max_tokens=512)
    messages =[("Write me a song about sparkling water.")]
    async def event_stream():
        for chunk in llm.stream(messages):
            yield f"data: {chunk}\n\n"
            
    response = StreamingResponse(event_stream(), media_type="text/event-stream")

    end_time = time.time()  # End timing

    # Calculate the time taken
    time_taken = end_time - start_time

    print(f"Time taken to generate response: {time_taken} seconds")

    return response
