import httpx
from fastapi import HTTPException

EMBEDDINGS_SERVICE_URL = "http://embeddings_service:8001/embed"

http_client = httpx.AsyncClient(timeout=10.0)

async def get_embeddings(texts: list[str]) -> list[list[float]]:
    try:
        response = await http_client.post(
            EMBEDDINGS_SERVICE_URL,
            json={"texts": texts}
        )
        response.raise_for_status()
        data = response.json()
        return data.get("embeddings", [])
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Error de conexión con embeddings_service: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error en embeddings_service: {e.response.text}")
