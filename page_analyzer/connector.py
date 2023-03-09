import psycopg2

from page_analyzer.seopage import SEOPage
from page_analyzer.seocheck import SEOCheck

class Connector:
    def __init__(self, connection_sring) -> None:
        self.connection = psycopg2.connect(connection_sring)
        self.connection.autocommit = True

    def get_page(self, name: str):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT name, id, created_at FROM urls WHERE name = %s', (name,))
            try:
                data = cursor.fetchone()
            except psycopg2.ProgrammingError as error:
                print(error)
                return None
            page = SEOPage(*data) if data else None
            return page

    def get_page_by_id(self, page_id):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT name, id, created_at FROM urls WHERE id = %s', (page_id,))
            try:
                data = cursor.fetchone()
            except psycopg2.ProgrammingError as error:
                print(error)
                return None
            page = SEOPage(*data) if data else None
            return page

    def get_pages(self):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT name, id, created_at FROM urls ORDER BY created_at DESC')
            try:
                data = cursor.fetchall()
            except psycopg2.ProgrammingError as error:
                print(error)
                return None
            pages = [SEOPage(*page) for page in data]
            return pages

    def add_page(self, page: SEOPage):
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)", (page.name, page.created_at))

    def add_check(self, check: SEOCheck):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
                (check.url_id, check.status_code, check.h1, check.title, check.description, check.created_at)
            )

    def get_checks_for_page(self, page_id):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT url_id, status_code, h1, title, description, id, created_at FROM url_checks WHERE url_id = %s ORDER BY id DESC', (page_id,))
            try:
                data = cursor.fetchall()
            except psycopg2.ProgrammingError as error:
                print(error)
                return None
            checks = [SEOCheck(*check) for check in data]
            return checks
    
    def get_last_check(self, page_id):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT url_id, status_code, h1, title, description, id, created_at FROM url_checks WHERE url_id = %s ORDER BY id DESC LIMIT 1', (page_id,))
            try:
                data = cursor.fetchone()
            except psycopg2.ProgrammingError as error:
                print(error)
                return None
            if not data:
                return None
            check = SEOCheck(*data)
            return check