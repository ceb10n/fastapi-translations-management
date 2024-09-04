import os
from enum import Enum, unique
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.progress import track

from fastapi_translations import printer
from fastapi_translations.git import FastAPIGitDocs
from fastapi_translations.models import DocFile, Summary

console = Console()

app = typer.Typer(rich_markup_mode="rich")


@unique
class Languages(Enum):
    az = "az"
    bn = "bn"
    de = "de"
    em = "em"
    es = "es"
    fa = "fa"
    fr = "fr"
    he = "he"
    hu = "hu"
    id = "id"
    it = "it"
    ja = "ja"
    ko = "ko"
    pl = "pl"
    pt = "pt"
    ru = "ru"
    tr = "tr"
    uk = "uk"
    ur = "ur"
    vi = "vi"
    yo = "yo"
    zh = "zh"
    zh_hant = "zh-hant"


@app.command("report")
def report(
    lang: Annotated[
        Languages,
        typer.Option(
            ...,
            "--language", "-l",
            help="The language to check for translations report"
        ),
    ],
    save_csv: Annotated[
        bool,
        typer.Option(
            "--csv", "-c",
            help="Save all missing and outdated translations to a csv file"
        )
    ] = False
) -> None:
    """Generate a report for the translated docs"""
    base_docs_path = Path("docs")
    en_docs_path = Path("docs/en")

    summary = Summary(lang=lang.value)
    console.clear()
    git = FastAPIGitDocs()

    for root, _, files in track(
        os.walk(en_docs_path),
        "🚶 Walking through 📂 docs looking for 🔠 translations",
    ):
        for file in files:
            if file.endswith(".md"):
                file_relative_path = os.path.relpath(
                    os.path.join(root, file), en_docs_path
                )
                translated_path = os.path.join(
                    base_docs_path, lang.value, file_relative_path
                )
                translation_exists = os.path.exists(translated_path)

                original_doc_date = git.get_commit_date_for(
                    os.path.join(root, file)
                )
                translation_is_outdated = False
                translated_date = git.get_commit_date_for(translated_path)

                if translated_date and original_doc_date:
                    translation_is_outdated = translated_date > original_doc_date

                doc = DocFile(
                    translation_lang=lang.value,
                    original_file=os.path.join(root, file),
                    original_commit=original_doc_date,
                    translation_file=translated_path,
                    translation_exists=translation_exists,
                    translation_commit=translated_date,
                    translation_is_outdated=translation_is_outdated
                )
                summary.append_file(doc)
    printer.print_table(summary, console, 10)

    if save_csv:
        printer.print_to_csv(summary)


def main() -> None:
    app()
