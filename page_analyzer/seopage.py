import datetime
from page_analyzer.seocheck import SEOCheck

class SEOPage:
    def __init__(self, name: str, page_id: int = 0, created_at: datetime.date = None) -> None:
        self.page_id = page_id
        self.name = name
        if not created_at:
            created_at = datetime.date.today()
        self.created_at = created_at
        self.checks = []

    def check(self):
        #connect to page
        return SEOCheck(self.page_id, 0, "STUB", "STUB", "STUB")