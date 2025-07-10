from datetime import datetime
from typing import Any, Dict

def serialize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    serialized = {}

    for k, v in metadata.items():
        if k == "date":
            if isinstance(v, str):
                try:
                    # Intenta parsear como fecha
                    dt = datetime.fromisoformat(v)
                    serialized[k] = dt.timestamp()
                except ValueError:
                    try:
                        serialized[k] = float(v)
                    except ValueError:
                        serialized[k] = v
            elif isinstance(v, datetime):
                serialized[k] = v.timestamp()
            elif isinstance(v, (int, float)):
                serialized[k] = float(v)
            else:
                serialized[k] = v
        else:
            serialized[k] = v

    return serialized
