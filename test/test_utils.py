import pytest
from src.domain.utils import base62_converter


def test_base62_converter():
    assert base62_converter(1) == "B"
