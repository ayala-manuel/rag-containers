from datetime import datetime, timedelta, timezone
from qdrant_client.http.models import Filter, FieldCondition, MatchAny, Range
from api.schemas import QueryMetadata
from typing import Optional

def build_filter(metadata: Optional[QueryMetadata]) -> Optional[Filter]:
    """
    Genera un Filter para Qdrant:
      - MatchAny sobre metadata.tags
      - Range sobre metadata.date (en ms UTC), ampliado ±30d si no hay date_2
    """
    if metadata is None:
        return None

    conditions = []

    # Filtrar por tags
    if metadata.tags:
        conditions.append(
            FieldCondition(
                key="metadata.tags",
                match=MatchAny(any=metadata.tags)
            )
        )

    # Filtrar por rango de fechas
    if metadata.date_1:
        # Parsear date_1 (ISO) y normalizar a UTC
        dt1 = datetime.fromisoformat(metadata.date_1)
        dt1 = dt1.replace(tzinfo=timezone.utc)

        # Si hay date_2 la parseamos, si no usamos ±30 días
        if metadata.date_2:
            dt2 = datetime.fromisoformat(metadata.date_2)
            dt2 = dt2.replace(tzinfo=timezone.utc)
        else:
            dt2 = dt1 + timedelta(days=30)
            dt1 = dt1 - timedelta(days=30)

        ms1 = int(dt1.timestamp() * 1000)
        ms2 = int(dt2.timestamp() * 1000)

        conditions.append(
            FieldCondition(
                key="metadata.date",
                range=Range(gte=ms1, lte=ms2)
            )
        )

    return Filter(must=conditions) if conditions else None