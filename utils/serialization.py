from datetime import datetime, timezone
from typing import Any, Dict, Union, Optional

def serialize_metadata(metadata: Dict[str, Any]) -> Dict[str, Union[Any, int, None]]:
    """
    Convierte cualquier campo cuya clave contenga 'date' a timestamp UTC en milisegundos.
    Otros campos se devuelven tal cual.
    """
    serialized: Dict[str, Union[Any, int, None]] = {}

    for key, val in metadata.items():
        if 'date' in key.lower():
            ts: Optional[int]
            try:
                # Si viene como str en formato ISO (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS)
                if isinstance(val, str):
                    # fromisoformat acepta ambos formatos
                    dt = datetime.fromisoformat(val)
                else:
                    dt = val  # asume que ya es datetime

                # Forzar UTC (si no tiene tzinfo, se asume UTC)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                else:
                    dt = dt.astimezone(timezone.utc)

                ts = int(dt.timestamp() * 1000)
            except Exception:
                # Si no pudo parsear, intentar como número bruto (ms)
                try:
                    ts = int(float(val))
                except Exception:
                    ts = None
            serialized[key] = ts
        else:
            serialized[key] = val

    return serialized
