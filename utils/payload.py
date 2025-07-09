# utils/payload.py

from typing import List, Dict
from utils.chunking import text_splitter
from utils.serialization import serialize_metadata
from utils.embedding_client import get_embeddings

def build_payload(
        data: List[Dict[str, str]],
        max_words: int = 1000,
        overlap: int = 100
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
    try:
        payloads = []
        for doc in data:
            text = doc.text
            metadata = doc.metadata.dict() if doc.metadata else {}
            chunks = text_splitter(text, max_words=max_words, overlap=overlap)
            serialized_metadata = serialize_metadata(metadata)

            for chunk in chunks:
                payloads.append({
                    "text": chunk,
                    "embedding": get_embeddings(chunk),
                    "metadata": serialized_metadata
                })
        return payloads
    except Exception as e:
        return [{"error": str(e)}]