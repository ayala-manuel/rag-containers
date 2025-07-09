from datetime import datetime
from typing import Any, Dict

def serialize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    serialized = {}
    for k, v in metadata.items():
        if isinstance(v, datetime):
            serialized[k] = v.isoformat()
        else:
            serialized[k] = v
    return serialized