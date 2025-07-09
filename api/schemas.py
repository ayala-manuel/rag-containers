from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CreateCollectionRequest(BaseModel):
    name: str

class Metadata(BaseModel):
    title: str = Field(..., description="Título del documento")
    date: datetime = Field(..., description="Fecha asociada al documento")
    tags: List[str] = Field(..., description="Lista de etiquetas")
    images: Optional[List[str]] = Field(None, description="URLs o identificadores de imágenes")

class DocumentItem(BaseModel):
    text: str = Field(..., description="Texto completo del documento")
    metadata: Optional[Metadata] = Field(None, description="Metadatos asociados al documento")


class SearchRequest(BaseModel):
    query_vector: List[float]
    limit: int = 10