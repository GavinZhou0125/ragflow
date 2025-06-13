import logging
from urllib.parse import parse_qs, urlparse
from api.db.services.file_service import FileService
from rag.utils.storage_factory import STORAGE_IMPL


_logger = logging.getLogger("file_url_utils")

class StoredFileObj:
    _bucket: str
    _name: str
    _original_file_name: str | None = None

    def __init__(self, bucket: str, name: str, original_file_name: str | None = None) -> None:
        self._bucket = bucket
        self._name = name
        self._original_file_name = original_file_name

    @property
    def filename(self) -> str:
        return self._original_file_name or ""

    def read(self) -> bytes:
        return STORAGE_IMPL.get(self._bucket, self._name)


def is_stored_url(url: str) -> bool:
    return url.startswith("stored://")


def parse_from_file_urls(urls: str | list[str], user_id: str) -> list[str]:
    if isinstance(urls, str):
        urls = urls.split("\n")

    results: list[str] = []

    for url in urls:
        file_obj = None

        if is_stored_url(url):
            parsed_url = urlparse(url)
            parsed_qs = parse_qs(parsed_url.query)
            bucket, name = parsed_url.path[1:].split("/")
            original_file_name = parsed_qs["originalname"][0]
            result: str

            if original_file_name:
                result = original_file_name + "\n"
            else:
                result = ""

            _logger.info("Resolved url %s to bucket %s name %s", url, bucket, name)
            file_obj = StoredFileObj(bucket, name, original_file_name)
        else:
            raise ValueError(f"Unsupported url {url}")

        result += FileService.parse_docs([file_obj], user_id)
        results.append(result)

    return results
