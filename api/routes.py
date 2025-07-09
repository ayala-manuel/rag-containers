# api/routes.py

from fastapi import APIRouter, Depends, HTTPException, Path, Body
from api.schemas import (
    CreateCollectionRequest,
    DocumentItem,
    SearchRequest
    )
from core.client import (
    return_collection_names,
    create_collection,
    delete_collection,
    insert_data,
    search
)
from api.dependencies import verify_api_key
from utils.payload import build_payload
from typing import List

# TODO: EMBEDDING GENERATION ?
router = APIRouter()

@router.get("/", summary="Bienvenida a la API de Mercados Qdrant")
async def welcome():
    """
    Endpoint de bienvenida que devuelve un mensaje de bienvenida.
    """
    return {
        "message": "Bienvenido a la API de Mercados Qdrant",
        "version": "1.0.0",
        "description": "El API se encuentra corriendo correctamente",
    }

@router.get("/ping")
async def ping():
    """
    Endpoint de prueba para verificar que la API está funcionando.
    """
    return {"message": "Pong"}

@router.get("/collections", dependencies=[Depends(verify_api_key)], summary="Listar todas las colecciones")
async def list_collections():
    """
    Devuelve las colecciones de la base de datos.
    """
    collections = return_collection_names()
    if isinstance(collections, dict) and "error" in collections:
        return {
            "status": "error",
            "message": "Error al obtener colecciones",
            "detail": collections["error"]
        }

    return {
        "status": "success",
        "data": collections,
        "message": f"{len(collections)} colección(es) encontradas"
    }

@router.post("/collections/create", dependencies=[Depends(verify_api_key)] , summary="Crear una nueva colección")
async def create_new_collection(payload: CreateCollectionRequest):
    """
    Crea una nueva colección en Qdrant con el nombre proporcionado.
    """
    result = create_collection(payload.name)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "status": "success",
        "message": f"Colección '{payload.name}' creada exitosamente",
        "collection": {
            "name": payload.name
        }
    }

@router.delete("/collections/{collection_name}", dependencies=[Depends(verify_api_key)], summary="Eliminar colección")
async def delete_existing_collection(collection_name: str = Path(..., description="Nombre de la colección a eliminar")):
    result = delete_collection(collection_name)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "status": "success",
        "message": f"Colección '{collection_name}' eliminada exitosamente"
    }

@router.post("/collections/{collection_name}/upload", summary="Subir documentos a una colección")
async def upload_documents(
    collection_name: str = Path(..., description="Nombre de la colección"),
    data: List[DocumentItem] = Body(..., description="Lista de documentos a subir")
):
    if not data:
        raise HTTPException(status_code=400, detail="No se proporcionaron documentos para subir")

    payloads = build_payload(data)
    
    # Verificar si hay error en alguno de los payloads
    for item in payloads:
        if "error" in item:
            raise HTTPException(status_code=400, detail=item["error"])
    
    # Insertar cada chunk
    for item in payloads:
        insert_result = insert_data(collection_name, item)
        if "error" in insert_result:
            raise HTTPException(status_code=500, detail=f"Error insertando datos: {insert_result['error']}")

    return {
        "status": "success",
        "message": f"{len(payloads)} fragmento(s) subido(s) a la colección '{collection_name}'"
    }

@router.post("/collections/{collection_name}/search", summary="Buscar documentos en una colección")
async def search_collection(collection_name: str, body: SearchRequest):
    response = search(collection_name, body.query_vector, body.limit)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    return {
        "status": "success",
        "message": "Search completed",
        "data": {
            "collection_name": response["collection_name"],
            "results": response["results"]
        }
    }