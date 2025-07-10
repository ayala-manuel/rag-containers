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

        # Convert to UNIX timestamps
        timestamp_1 = date_1.timestamp()
        timestamp_2 = date_2.timestamp()

        conditions.append(
            FieldCondition(
                key="date",
                range=Range(
                    gte=timestamp_1,
                    lte=timestamp_2
                )
            )
        )

    return Filter(must=conditions) if conditions else None