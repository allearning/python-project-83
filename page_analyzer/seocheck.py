import datetime


class SEOCheck:
    def __init__(
        self, url_id: int, status_code: int, h1: str, title: str,
        description: str, check_id: int = 0, created_at: datetime.date = None) -> None:
        self.url_id = url_id
        self.id = check_id
        self.status_code = status_code
        self.h1 = h1
        self.title = title
        self.description = description
        if not created_at:
            created_at = datetime.date.today()
        self.created_at = created_at
