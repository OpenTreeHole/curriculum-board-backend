from dataclasses import dataclass, field
from typing import List

from .review import Review


@dataclass
class Course:
    name: str
    credit: float
    review_list: List[Review] = field(default_factory=list)
