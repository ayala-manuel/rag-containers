from pydantic import BaseModel, Field
from typing import List, Optional

class CreateCollectionRequest(BaseModel):
    name: str
    vectorsize: int = Field(384, description="Tamaño del vector para la colección, por defecto 384")

class Metadata(BaseModel):
    title: str = Field(..., description="Título del documento")
    date: str = Field(..., description="Fecha asociada al documento")
    tags: List[str] = Field(..., description="Lista de etiquetas")
    url : Optional[str] = Field(None, description="URL del documento")
    images: Optional[List[str]] = Field(None, description="URLs o identificadores de imágenes")

class DocumentItem(BaseModel):
    text: str = Field(..., description="Texto completo del documento")
    metadata: Optional[Metadata] = Field(None, description="Metadatos asociados al documento")

class QueryMetadata(BaseModel):
    tags: Optional[List[str]] = Field(None, description="Lista de etiquetas para filtrar resultados")
    date_1: Optional[str] = Field(None, description="Fecha de inicio en formato YYYY-MM-DD")
    date_2: Optional[str] = Field(None, description="Fecha de fin en formato YYYY-MM-DD")

class SearchRequest(BaseModel):
    query: str = Field(..., description="Texto de consulta para generar el vector de búsqueda")
    metadata : Optional[QueryMetadata] = Field(None, description="Metadatos opcionales para filtrar resultados")
    limit: int = Field(10, description="Número máximo de resultados a retornar")

class EmbeddingsRequest(BaseModel):
    texts: List[str]

class EmbeddingsResponse(BaseModel):
    embeddings: List[List[float]]

class TitlesToDelete(BaseModel):
    titles: List[str]