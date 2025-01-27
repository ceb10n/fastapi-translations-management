from datetime import datetime

from pydantic import BaseModel


class Document(BaseModel):
    official_lang: str = "en"
    translation_lang: str
    original_file: str
    original_commit: datetime | None
    translation_file: str | None = None
    translation_exists: bool
    translation_commit: datetime | None
    translation_is_outdated: bool
