import datetime


class SEOPage:
    def __init__(self, name: str, id: int = 0, created_at: datetime.date = None) -> None:
        self.id = id
        self.name = name
        if not created_at:
            created_at = datetime.date.today()
        self.created_at = created_at
