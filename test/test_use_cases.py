import pytest
from src.application.ports.url_repository import URL_Repository
from src.application.use_cases.shorten_url import UseCaseShortenUrl
from src.domain.base62_converter import base62_converter
from src.domain.url import Url

class FakeUrlRepository(URL_Repository):
    def __init__(self):
        self.db_urls = {}
        self.db_alias = {}
        self.db_id_counter = 1

    def save_url(self, url) -> int:
        new_id = self.db_id_counter
        self.db_urls[new_id] = url
        self.db_id_counter += 1
        return new_id
    
    def update_url_alias(self, url_id, alias) -> None:
        original_url = self.db_urls[url_id]
        new_url = Url(original_url, aliases=alias)
        self.db_alias[alias] = new_url

    def get_url_by_alias(self, alias):
        return self.db_alias.get(alias)


def test_shorten_url():
    fake_repo = FakeUrlRepository()
    use_case = UseCaseShortenUrl(fake_repo)
    long_url = "https://www.midominio.com/mi-portafolio"


    use_case.execute(long_url)

    saved_url = fake_repo.get_url_by_alias('B')

    assert saved_url is not None
    assert saved_url.aliases == 'B'
    assert saved_url.url_link == long_url
