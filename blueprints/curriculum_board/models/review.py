from dataclasses import dataclass
from datetime import datetime


@dataclass
class Review:
    title: str
    reviewer_id: int
    time_created: datetime
    rank: str
    remark: int
