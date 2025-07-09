# utils/embedding_client.py

from pydantic import BaseModel
from typing import List
import httpx

class EmbeddingsRequest(BaseModel):
    texts: List[str]

class EmbeddingsResponse(BaseModel):
    embeddings: List[List[float]]

http_client = httpx.AsyncClient(timeout=10.0)

async def embed_texts(request: EmbeddingsRequest):
    url = "http://embeddings_service:8001/embed"
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.post(url, json={"texts": request.texts})
            response.raise_for_status()
            data = response.json()
            response =  EmbeddingsResponse(embeddings=data.get("embeddings", []))
            return response["embeddings"][0]
        except httpx.RequestError as e:
            return {"error": f"Error connecting to embeddings_service: {str(e)}"}
