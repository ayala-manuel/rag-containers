from datetime import datetime, timedelta, timezone
from qdrant_client.http.models import Filter, FieldCondition, MatchAny, Range
from utils.utils import datetime_to_iso_z
from api.schemas import QueryMetadata
from typing import Optional

def build_filter(metadata: Optional[QueryMetadata]) -> Optional[Filter]:
    if metadata is None:
        return None

    conditions = []

    # 1. Tags
    if metadata.tags:
        conditions.append(
            FieldCondition(
                key="tags",
                match=MatchAny(any=metadata.tags)
            )
        )

    # 2. Dates
    if metadata.date_1:
        date_format = "%Y-%m-%d"
        date_1 = datetime.strptime(metadata.date_1, date_format).replace(tzinfo=timezone.utc)

        if metadata.date_2:
            date_2 = datetime.strptime(metadata.date_2, date_format).replace(tzinfo=timezone.utc)
        else:
            date_2 = date_1 + timedelta(days=30)
            date_1 = date_1 - timedelta(days=30)

        conditions.append(
            FieldCondition(
                key="date",
                range=Range(
                    gte=datetime_to_iso_z(date_1),
                    lte=datetime_to_iso_z(date_2)
                )
            )
        )

    return Filter(must=conditions) if conditions else None