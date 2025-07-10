from datetime import datetime, timedelta, timezone
from qdrant_client.http.models import Filter, FieldCondition, MatchAny, Range
from api.schemas import QueryMetadata
from typing import Optional

def build_filter(metadata: Optional[QueryMetadata]) -> Optional[Filter]:
    if metadata is None:
        return None

    conditions = []

    if metadata.tags:
        conditions.append(
            FieldCondition(
                key="tags",
                match=MatchAny(any=metadata.tags)
            )
        )

    if metadata.date_1:
        date_format = "%Y-%m-%d"
        date_1 = datetime.strptime(metadata.date_1, date_format).replace(tzinfo=timezone.utc)
        if metadata.date_2:
            date_2 = datetime.strptime(metadata.date_2, date_format).replace(tzinfo=timezone.utc)
        else:
            date_2 = date_1 + timedelta(days=30)
            date_1 = date_1 - timedelta(days=30)

        gte_str = date_1.isoformat(timespec='seconds').replace('+00:00', 'Z')
        lte_str = (date_2 + timedelta(hours=23, minutes=59, seconds=59)).isoformat(timespec='seconds').replace('+00:00', 'Z')

        conditions.append(
            FieldCondition(
                key="date",
                range=Range(
                    gte=gte_str,
                    lte=lte_str
                )
            )
        )

    return Filter(must=conditions) if conditions else None