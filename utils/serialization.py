from datetime import datetime
from typing import Any, Dict

def serialize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    serialized = {}
    for k, v in metadata.items():
        if k == "date":
            if isinstance(v, str):
                # Si llega como string tipo "2025-07-10" o ISO, parsear
                try:
                    dt = datetime.fromisoformat(v)
                except ValueError:
                    dt = datetime.strptime(v, "%Y-%m-%d")
                serialized[k] = dt.timestamp()
            elif isinstance(v, datetime):
                serialized[k] = v.timestamp()
            else:
                serialized[k] = v  # Dejarlo como está si ya es numérico
        else:
            serialized[k] = v
    return serialized
