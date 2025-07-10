from datetime import datetime, timezone

def datetime_to_iso_z(dt: datetime) -> str:
    """
    Convierte un datetime a una cadena ISO 8601 UTC terminada en 'Z',
    como la que usa Qdrant: 'YYYY-MM-DDTHH:MM:SSZ'
    
    Asegura que el objeto tenga zona horaria UTC.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)

    return dt.isoformat(timespec='seconds').replace("+00:00", "Z")
