import psycopg2

from page_analyzer.seopage import SEOPage


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

    def get_page_by_id(self, id):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT name, id, created_at FROM urls WHERE id = %s', (id,))
            try:
                data = cursor.fetchone()
            except psycopg2.ProgrammingError as error:
                print(error)
                return None
            page = SEOPage(*data)
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
