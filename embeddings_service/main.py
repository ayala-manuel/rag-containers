from fastapi import FastAPI, HTTPException
from embeddings_service.schemas import TextRequest, EmbeddingResponse
from sentence_transformers import SentenceTransformer
from utils.env import load_env, get_env_var
import asyncio

load_env()
model_name = get_env_var("EMBED_MODEL", default="all-MiniLM-L6-v2")
model = SentenceTransformer(model_name)

app = FastAPI(title="Embeddings Service", version="1.0.0")

@app.post("/embed", response_model=EmbeddingResponse)
async def embed_texts(request: TextRequest):
    if not request.texts:
        raise HTTPException(status_code=400, detail="No texts provided")

    try:
        embeddings = await asyncio.to_thread(lambda: model.encode(request.texts))

        return EmbeddingResponse(embeddings=embeddings.tolist())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")
