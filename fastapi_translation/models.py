from pydantic import BaseModel

class DocFile(BaseModel):
    official_lang: str = "en"
    translation_lang: str
    original_file: str
    translation_file: str | None = None
    translation_exists: bool

class Summary(BaseModel):
    lang: str
    files_analyzed: int = 0
    files_translated: int = 0
    files: list[DocFile] = []

    def append_file(self, doc: DocFile) -> None:
        self.files.append(doc)
        self.files_analyzed += 1

        if doc.translation_exists:
            self.files_translated += 1

