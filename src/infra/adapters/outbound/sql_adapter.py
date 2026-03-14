import sqlite3

from src.application.ports.url_repository import URL_Repository
from src.domain.url import Url

class SQLAdapter(URL_Repository):
    def __init__(self, db_path: str = 'example.db'):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS urls
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_link TEXT NOT NULL,
                aliases TEXT ,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )

                 """)
            conn.commit()

    def save_url(self, url):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO urls (url_link)
                VALUES(?)
                """,(url,)
            )
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        
    def update_url_alias(self, url_id, alias):
          with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE urls
                SET aliases = (?)
                WHERE id = (?)
                """,
                (alias,url_id)
                )
            conn.commit()

    def get_url_by_alias(self, alias):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT url_link from urls
                WHERE aliases = ?
                """, (alias,))
            row = cursor.fetchone()
            if row is not None:
                return Url(url_link=row[0], aliases=alias)
            else:
                return None
         

            
            