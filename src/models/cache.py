from dataclasses import dataclass
from datetime import datetime


@dataclass
class Cache:
    last_udpdate: datetime
    date_in_cache: datetime
    data: dict