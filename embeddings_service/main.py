from fastapi import FastAPI, HTTPException
from embeddings_service.schemas import TextRequest, EmbeddingResponse
from sentence_transformers import SentenceTransformer
from utils.env import load_env, get_env_var

load_env()
model = get_env_var("EMBED_MODEL", default="all-MiniLM-L6-v2")

app = FastAPI(title="Embeddings Service", version="1.0.0")

@app.post("/embed", response_model=EmbeddingResponse)
async def embed_texts(request: TextRequest):
    if not request.texts:
        raise HTTPException(status_code=400, detail="No texts provided")
    
    try:
        embeddings = model.encode(request.texts, convert_to_numpy=True).tolist()
        return EmbeddingResponse(embeddings=embeddings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")
