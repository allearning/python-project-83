import datetime
import requests
from bs4 import BeautifulSoup
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

        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('title')
        title = title.string if title else ''

        h1 = soup.find('h1')
        h1 = h1.string if h1 else ''

        descr = soup.find('meta', attrs={'name': 'description'})
        descr = descr['content'] if descr else ''

        return SEOCheck(self.page_id, r.status_code, h1, title, descr)