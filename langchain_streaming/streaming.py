from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router import main_streaming_endpoint, chatopenai_streaming_endpoint, azureopenai_streaming_endpoint

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_streaming_endpoint.router, prefix="")
app.include_router(chatopenai_streaming_endpoint.router, prefix="")
app.include_router(azureopenai_streaming_endpoint.router, prefix="")