from datetime import datetime

from pydantic import BaseModel, computed_field


class Document(BaseModel):
    official_lang: str = "en"
    translation_lang: str
    original_file: str
    original_commit: datetime | None
    translation_file: str | None = None
    translation_exists: bool
    translation_commit: datetime | None

    @computed_field  # type: ignore
    @property
    def translation_is_outdated(self) -> bool:
        if not self.original_commit or not self.translation_commit:
            return False

        return self.original_commit > self.translation_commit
