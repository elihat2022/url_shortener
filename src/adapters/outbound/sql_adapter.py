import sqlite3
from typing import Optional
from src.ports.repository import UrlRepository
from src.domain.entities import Url


class SqlAdapter(UrlRepository):
    def __init__(self, db_path: str = 'urls.db'):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url_link TEXT NOT NULL,
                    aliases TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_url(self, url: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO urls (url_link) VALUES (?)", (url,))
            conn.commit()
            return cursor.lastrowid

    def update_url_alias(self, url_id: int, alias: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE urls SET aliases = ? WHERE id = ?", (alias, url_id))
            conn.commit()

    def get_url_by_alias(self, alias: str) -> Optional[Url]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT url_link FROM urls WHERE aliases = ?", (alias,))
            row = cursor.fetchone()
            if row:
                return Url(url_link=row[0], aliases=alias)
            return None
