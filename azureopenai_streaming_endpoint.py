from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware


from langchain_openai import AzureChatOpenAI

import os

app = FastAPI()

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

    response_text = ""
    model = AzureChatOpenAI(
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION_CHAT"),
        azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )
    messages =[("Tell me a joke about dogs")]

    chunks = []
    async def event_stream():
        async for chunk in model.astream(messages):
            chunks.append(chunk)
            yield f"data: {chunk.content}\n\n"
            
    return StreamingResponse(event_stream(), media_type="text/event-stream")