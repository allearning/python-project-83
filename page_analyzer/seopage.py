import datetime
import requests
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
        r = requests.get(self.name)
        content = r.text

        try:
            title_start = content.index('<title>') + len('<title>')
            title_end = content.index('</title>')
            title = content[title_start:title_end]
        except ValueError:
            title = ''
        try:
            h1_start = content.index('<h1>') + len('<h1>')
            h1_end = content.index('</h1>')
            h1 = content[h1_start:h1_end]
        except ValueError:
            h1 = ''

        try:
            descr_start = content.index('<meta name="description" content="') + len('<meta name="description" content="')
            descr_end = content.index('"', descr_start)
            descr = content[descr_start:descr_end]
        except ValueError:
            descr = ''
        return SEOCheck(self.page_id, r.status_code, h1, title, descr)