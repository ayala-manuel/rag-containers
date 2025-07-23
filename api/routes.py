# api/routes.py

from fastapi import APIRouter, Depends, HTTPException, Path, Body
from api.schemas import (
    CreateCollectionRequest,
    DocumentItem,
    SearchRequest,
    TitlesToDelete
    )
from core.client import (
    return_collection_names,
    create_collection,
    delete_collection,
    insert_data,
    search,
    get_collection_documents,
    delete_document_by_title
)
from api.dependencies import verify_api_key
from utils.payload import build_payload, build_query_vector
from utils.query_filters import build_filter
from typing import List

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
    result = create_collection(payload.name, payload.vectorsize)

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
    data: List[DocumentItem] = Body(..., description="Lista de documentos a subir"),
    chunk: bool = Body(True, description="Indica si se debe hacer chunking de los textos")
):
    if not data:
        raise HTTPException(status_code=400, detail="No se proporcionaron documentos para subir")

    payloads = await build_payload(data, chunk=chunk)

    # # Verificar si hay error en alguno de los payloads
    # for item in payloads:
    #     if "error" in item:
    #         raise HTTPException(status_code=400, detail=item["error"])
    
    # Insertar cada chunk
    result = insert_data(collection_name, payloads)
    if "error" in result:
        raise HTTPException(status_code=500, detail=f"Error insertando datos: {result['error']}")

    return {
        "status": "success",
        "message": f"{len(payloads)} fragmento(s) subido(s) a la colección '{collection_name}'"
    }

@router.post("/collections/{collection_name}/search", summary="Buscar documentos en una colección")
async def search_collection(collection_name: str, body: SearchRequest):
    try:
        query_vector = await build_query_vector(body.query)
        print(body.metadata)
        filters = build_filter(body.metadata)
        print("Filters:", filters)

        response = search(collection_name, query_vector, body.limit, filters, body.threshold)

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

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
    
@router.get("/collections/{collection_name}/docs", summary="Ver documentos en una colección")
async def get_documents(collection_name: str):
    """
    Obtiene todos los documentos de una colección.
    """
    try:
        documents = get_collection_documents(collection_name)
        if "error" in documents:
            raise HTTPException(status_code=500, detail=documents["error"])
        
        return {
            "status": "success",
            "message": f"Documents retrieved from collection '{collection_name}'",
            "data": documents
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")
    
@router.post("/collections/{collection_name}/docs/delete", summary="Eliminar documentos por títulos")
async def delete_documents(collection_name: str, body: TitlesToDelete):
    errors = []
    results = []
    for title in body.titles:
        result = delete_document_by_title(collection_name, title)
        if "error" in result:
            errors.append({"title": title, "error": result["error"]})
        else:
            results.append(result)

    if errors:
        return {
            "status": "partial_success",
            "message": "Algunos documentos no pudieron ser eliminados",
            "errors": errors,
            "results": results
        }
    return {
        "status": "success",
        "message": "Documentos eliminados correctamente",
        "results": results
    }