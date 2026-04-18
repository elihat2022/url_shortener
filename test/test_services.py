import pytest
from src.ports.repository import UrlRepository
from src.domain.services import UrlShortenerService
from src.domain.entities import Url


class FakeUrlRepository(UrlRepository):
    def __init__(self):
        self.db_urls = {}
        self.db_alias = {}
        self.db_id_counter = 1

    def save_url(self, url: str) -> int:
        new_id = self.db_id_counter
        self.db_urls[new_id] = url
        self.db_id_counter += 1
        return new_id

    def update_url_alias(self, url_id: int, alias: str) -> None:
        original_url = self.db_urls[url_id]
        new_url = Url(original_url, aliases=alias)
        self.db_alias[alias] = new_url

    def get_url_by_alias(self, alias: str) -> Url:
        return self.db_alias.get(alias)


def test_shorten_url():
    fake_repo = FakeUrlRepository()
    service = UrlShortenerService(fake_repo)
    long_url = "https://www.midominio.com/mi-portafolio"

    result = service.execute(long_url)

    assert result is not None
    assert result.aliases == 'B'
    assert result.url_link == long_url
