import pytest
from src.domain.base62_converter import base62_converter

def test_base62_converter():
    assert base62_converter(1) == "B"
