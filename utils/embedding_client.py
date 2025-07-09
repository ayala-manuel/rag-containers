# utils/embedding_client.py

import httpx

EMBEDDINGS_SERVICE_URL = "http://embeddings_service:8001/embed"

async def get_embeddings(texts: list[str]) -> list[list[float]]:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(EMBEDDINGS_SERVICE_URL, json={"texts": texts})
        response.raise_for_status()
        data = response.json()
        return data.get("embeddings", [])
