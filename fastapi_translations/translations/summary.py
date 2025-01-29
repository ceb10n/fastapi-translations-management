import fnmatch
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pydantic import BaseModel, computed_field
from rich.progress import Progress, TaskID

from ..git import FastAPIGitDocs
from .document import Document

base_docs_path = Path("docs")
"""The base path for FastAPI documentation."""

en_docs_path = Path("docs/en")
"""The base path for FastAPI english documentation;"""

restricted_list = [
    "*reference/*",
    "*release-notes.md",
    "*fastapi-people.md",
    "*external-links.md",
    "*newsletter.md",
    "*management-tasks.md",
    "*management.md",
    "*contributing.md",
]
"""list[str]: Restricted files and/or folders.

FastAPI docs states that not all documents should be translated.
You can find the reference in `Contributing`_.

.. _Contributing: https://fastapi.tiangolo.com/contributing/#dont-translate-these-pages
"""


class Summary(BaseModel):
    lang: str
    files_analyzed: int = 0
    files_translated: int = 0
    files_outdated: int = 0
    files_missing_translation: int = 0
    files: list[Document] = []

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

    def generate(self) -> None:
        git = FastAPIGitDocs()
        with Progress() as progress:
            futures = []

            for root, _, files in os.walk(en_docs_path):
                if root.startswith("docs/en/docs/img") or root.startswith(
                    "docs/en/docs/js"
                ):
                    continue

                task = progress.add_task(
                    f"🚶 Walking through 📂 {root} looking for 🔠 translations",
                    start=False,
                )
                with ThreadPoolExecutor(max_workers=50) as pool:
                    future = pool.submit(
                        self.process_file, git, root, files, progress, task
                    )
                    futures.append(future)

    def process_file(
        self,
        git: FastAPIGitDocs,
        root_dir: str,
        files: list[str],
        progress: Progress,
        task: TaskID,
    ) -> None:
        progress.update(task, total=len(files))
        progress.start_task(task)

        for file in files:
            if file.endswith(".md"):
                file_relative_path = os.path.relpath(
                    os.path.join(root_dir, file), en_docs_path
                )
                if self.file_in_reserved_list(file_relative_path):
                    progress.update(task, advance=1)
                    continue

                translated_path = os.path.join(
                    base_docs_path, self.lang, file_relative_path
                )
                translation_exists = os.path.exists(translated_path)

                original_doc_date = git.get_commit_date_for(
                    os.path.join(root_dir, file)
                )

                translated_date = git.get_commit_date_for(translated_path)

                document = Document(
                    translation_lang=self.lang,
                    original_file=os.path.join(root_dir, file),
                    original_commit=original_doc_date,
                    translation_file=translated_path,
                    translation_exists=translation_exists,
                    translation_commit=translated_date,
                )
                self.append_document(document)

            progress.update(task, advance=1)

    def file_in_reserved_list(self, file: str) -> bool:
        for reserved in restricted_list:
            if fnmatch.fnmatch(file, reserved):
                return True

        return False

    def append_document(self, doc: Document) -> None:
        self.files.append(doc)
        self.files_analyzed += 1

        if doc.translation_exists:
            self.files_translated += 1

        if not doc.translation_exists:
            self.files_missing_translation += 1

        if doc.translation_is_outdated:
            self.files_outdated += 1

    def first_outdated_files(self, lenght: int = 10) -> list[Document]:
        return list(filter(lambda d: d.translation_is_outdated, self.files))[
            :lenght
        ]

    def first_missing_translation_files(
        self, lenght: int = 10
    ) -> list[Document]:
        return list(filter(lambda d: not d.translation_exists, self.files))[
            :lenght
        ]
