from datetime import datetime, timezone
from dataclasses import dataclass, field


@dataclass
class Url:
    url_link: str
    aliases: str
    creation_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
