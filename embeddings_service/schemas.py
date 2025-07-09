from pydantic import BaseModel, Field
from typing import List

class TextRequest(BaseModel):
    texts: List[str] = Field(..., example=["Hola mundo", "Texto de ejemplo"])

class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]] = Field(..., example=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
