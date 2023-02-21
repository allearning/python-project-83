"""Module with validators
"""
from typing import List
from urllib.parse import urlparse
import validators


def validate_url(url: str) -> List[str]:
    errors = []
    if not validators.url(url, public=False):
        errors.append('Некорректный URL')
    if url == '':
        errors.append('URL обязателен')
    if len(url) > 255:
        errors.append('URL превышает 255 символов')
    return errors


def cut_netloc(url: str) -> str:
    url_components = urlparse(url)
    return f'{url_components.scheme}://{url_components.netloc}'
