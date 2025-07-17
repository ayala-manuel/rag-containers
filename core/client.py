# core/client.py

from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    PointIdsList
)
from utils.ids import generate_uuid4
from utils.serialization import serialize_metadata
import numpy as np

client = QdrantClient(
    host="qdrant",
    port= 6333
)

def create_collection(collection_name: str):
    """
    Create a collection in Qdrant with the specified name.
    """
    try:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,  # TODO: Comprobar que embeddings utilizar y ajustar el tamaño
                distance=Distance.COSINE
            )
        )
        return {"status": "Collection created successfully", "collection_name": collection_name}
    except Exception as e:
        return {"error": str(e), "collection_name": collection_name}

def delete_collection(collection_name: str):
    try:
        client.delete_collection(collection_name=collection_name)
        return {"status": "Collection deleted successfully", "collection_name": collection_name}
    except Exception as e:
        return {"error": str(e), "collection_name": collection_name}

def insert_data(collection_name: str, data: list):
    """
    Inserta una lista de documentos en la colección especificada de Qdrant.

    Cada documento debe ser un dict con:
      - 'embedding': lista de floats (vector embebido)
      - 'text': texto asociado al documento
      - 'metadata': dict opcional con campos adicionales (title, date, tags, etc.)

    La función serializa automáticamente los campos datetime en metadata
    para que sean compatibles con el formato JSON de Qdrant.

    Args:
        collection_name (str): Nombre de la colección en Qdrant.
        data (list): Lista de documentos con embedding, text y metadata.

    Returns:
        dict: Resultado del upsert o error en caso de excepción.
    """
    try:
        points = [
            PointStruct(
                id=generate_uuid4(),
                vector=item["embedding"],
                payload={
                    "text": item["text"],
                    "metadata": serialize_metadata(item.get("metadata", {}))
                }
            ) for item in data
        ]

        client.upsert(
            collection_name=collection_name,
            points=points
        )
        return {
            "status": "Data inserted successfully",
            "collection_name": collection_name,
            "num_points": len(points)
        }
    except Exception as e:
        return {
            "error": str(e),
            "collection_name": collection_name
        }
    
def search(collection_name: str, query_vector: list, limit: int = 10, filters = None):
    """
    Search for similar vectors in the specified collection.
    """
    try:
        results = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=filters if filters else None,
            score_threshold=0.6
        )
        return {
            "status": "Search completed",
            "collection_name": collection_name,
            "results": [
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                } for result in results
            ]
        }
    except Exception as e:
        return {"error": str(e), "collection_name": collection_name}

def return_collection_names():
    try:
        collections = client.get_collections().collections
        return [
            {"collection_name": col.name}
            for col in collections
        ]
    except Exception as e:
        return {"error": str(e)}
    
def get_collection_documents(collection_name: str):
    """
    Returns all documents in the specified collection, grouped by metadata 'title'.
    """
    try:
        points, _ = client.scroll(
            collection_name=collection_name,
            limit=1000  # Adjust as needed
        )
        grouped = {}
        for point in points:
            title = None
            metadata = point.payload.get("metadata", {})
            if isinstance(metadata, dict):
                title = metadata.get("title")
            if title not in grouped:
                grouped[title] = []
            grouped[title].append({
                "id": point.id,
                "payload": point.payload
            })
        return {
            "status": "Documents retrieved and grouped by title successfully",
            "collection_name": collection_name,
            "documents_by_title": grouped
        }
    except Exception as e:
        return {"error": str(e), "collection_name": collection_name}
    
def delete_document_by_title(collection_name: str, title: str):
    """
    Deletes all documents in the specified collection with the given title in metadata.
    """
    try:
        points, _ = client.scroll(
            collection_name=collection_name,
            limit=1000  # Adjust as needed
        )
        ids_to_delete = [
            point.id for point in points
            if point.payload.get("metadata", {}).get("title") == title
        ]
        
        if not ids_to_delete:
            return {"status": "No documents found with the specified title", "collection_name": collection_name}
        
        client.delete(
            collection_name=collection_name,
            points_selector=PointIdsList(points=ids_to_delete)
        )
        
        return {
            "status": f"Documents with title '{title}' deleted successfully",
            "collection_name": collection_name,
            "deleted_ids": ids_to_delete
        }
    except Exception as e:
        return {"error": str(e), "collection_name": collection_name}