from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

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
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": "Tell me a joke about dogs"
            }],
        stream=True,
    )
    async def event_stream():
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield f"data: {content}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")