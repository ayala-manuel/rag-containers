# utils/payload.py

from typing import List, Dict
from utils.chunking import text_splitter
from utils.serialization import serialize_metadata
from utils.embedding_client import get_embeddings

async def build_payload(
        data: List[Dict[str, str]],
        max_words: int = 1000,
        overlap: int = 100,
        chunk : bool = True
) -> List[Dict]:
    """
    Procesa un documento para dividirlo en chunks, obtener embeddings y preparar payloads.

    Args:
        data (List[Dict]): Lista de documentos, donde cada documento es un dict con keys:
            - "text" (str): Texto a chunkear.
            - "metadata" (dict): Metadatos asociados al texto.
        max_words (int): Máximo número de palabras por chunk.
        overlap (int): Número de palabras solapadas entre chunks.

    Returns:
        List[Dict]: Lista de payloads con keys:
            - "text": fragmento de texto chunked.
            - "embeddings": vector embedding del chunk.
            - "metadata": metadatos serializados.
    """
    payloads = []
    try:
        if not chunk:
            text = data[0].text
            metadata = data[0].metadata.dict() if data[0].metadata else {}
            all_chunks = [text]
            all_metadata = [serialize_metadata(metadata)]
            embeddings = await get_embeddings(all_chunks)

            for chunk, embedding, metadata in zip(all_chunks, embeddings, all_metadata):
                payloads.append({
                    "text": chunk,
                    "embedding": embedding,
                    "metadata": metadata
                })
            return payloads
                
        else:
            all_chunks = []
            all_metadata = []
            # Si se requiere chunking, procesar cada documento
            for doc in data:
                text = doc.text
                metadata = doc.metadata.dict() if doc.metadata else {}
                chunks = text_splitter(text, max_words=max_words, overlap=overlap)

                all_chunks.extend(chunks)
                all_metadata.extend([serialize_metadata(metadata)] * len(chunks))

            embeddings = await get_embeddings(all_chunks)

            for chunk, embedding, metadata in zip(all_chunks, embeddings, all_metadata):
                payloads.append({
                    "text": chunk,
                    "embedding": embedding,
                    "metadata": metadata
                })

            return payloads
    except Exception as e:
        return [{"error": str(e)}]
    
async def build_query_vector(query: str) -> list:
    """
    Genera un vector de embedding para una consulta de búsqueda.

    Args:
        query (str): Texto de búsqueda.

    Returns:
        list: Vector de embedding correspondiente al query.
    """
    try:
        embeddings = await get_embeddings([query])
        return embeddings[0]
    except Exception as e:
        raise RuntimeError(f"Error generating query embedding: {str(e)}")