from datetime import datetime

from pydantic import BaseModel, computed_field


class DocFile(BaseModel):
    official_lang: str = "en"
    translation_lang: str
    original_file: str
    original_commit: datetime | None
    translation_file: str | None = None
    translation_exists: bool
    translation_commit: datetime | None
    translation_is_outdated: bool


class Summary(BaseModel):
    lang: str
    files_analyzed: int = 0
    files_translated: int = 0
    files_outdated: int = 0
    files_missing_translation: int = 0
    files: list[DocFile] = []

    @computed_field  # type: ignore
    @property
    def percentage_translated(self) -> float:
        try:
            return (
                100 * float(self.files_translated) / float(self.files_analyzed)
            )
        except Exception:
            return 0.0

    @computed_field  # type: ignore
    @property
    def percentage_missing_translation(self) -> float:
        try:
            return (
                100
                * float(self.files_missing_translation)
                / float(self.files_analyzed)
            )
        except Exception:
            return 0.0

    @computed_field  # type: ignore
    @property
    def percentage_outdated_translation(self) -> float:
        try:
            return 100 * float(self.files_outdated) / float(self.files_analyzed)
        except Exception:
            return 0.0

    def append_file(self, doc: DocFile) -> None:
        self.files.append(doc)
        self.files_analyzed += 1

        if doc.translation_exists:
            self.files_translated += 1

        if not doc.translation_exists:
            self.files_missing_translation += 1

        if doc.translation_is_outdated:
            self.files_outdated += 1

    def first_outdated_files(self, lenght: int = 10) -> list[DocFile]:
        return list(filter(lambda d: d.translation_is_outdated, self.files))[
            :lenght
        ]

    def first_missing_translation_files(
        self, lenght: int = 10
    ) -> list[DocFile]:
        return list(filter(lambda d: not d.translation_exists, self.files))[
            :lenght
        ]
