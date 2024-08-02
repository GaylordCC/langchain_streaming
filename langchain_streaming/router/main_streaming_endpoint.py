from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI

router = APIRouter(
    tags=['Chat-Completions-Streaming']
)
client = AsyncOpenAI()

@router.get("/main-streaming-endpoint")
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