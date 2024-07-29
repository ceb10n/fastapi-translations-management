import os

from typing import Annotated, Optional
from pathlib import Path

import typer

from git import Repo
from rich import print

from fastapi_translation.models import DocFile, Summary

app = typer.Typer()


base_docs_path = Path("docs")
en_docs_path = Path("docs/en")

def get_last_commit_date(repo_path, file_path):
    """
    Function to get the last commit date of a specific file in a repository
    """
    try:
        repo = Repo(repo_path, search_parent_directories=True)
        commits = list(repo.iter_commits(paths=file_path, max_count=1))
        if commits:
            return commits[0].committed_datetime
    except Exception as e:
        print(f"Error accessing the repository or file: {e}")
    return None


def compare_commits(en_repo_path, lang_repo_path, en_file, lang_file):
    """
    Function to compare the last commit dates of the English and translated files
    """
    en_date = get_last_commit_date(en_repo_path, en_file)
    lang_date = get_last_commit_date(lang_repo_path, lang_file)

    if en_date and lang_date:
        if en_date > lang_date:
            return en_file, lang_file, en_date, lang_date
    elif en_date:
        return en_file, lang_file, en_date, "Does not exist"
    return None


@app.command()
def report(lang: Annotated[Optional[str], typer.Argument(help="The language to check for translations report")] = None):
    """
    Generate a report for the translations of the given language compared to the
    official english docs.
    """
    if not lang:
        lang = "pt"
    summary = Summary(lang=lang)
    print(f"Walking through {base_docs_path} looking for markdown files")

    for root, dirs, files in os.walk(en_docs_path):
        for file in files:
            # if file.endswith(".md"):
            file_relative_path = os.path.relpath(os.path.join(root, file), en_docs_path)
            translated_path = os.path.join(base_docs_path, lang, file_relative_path)
            doc = DocFile(
                translation_lang=lang,
                original_file=os.path.join(root, file),
                translation_file=translated_path,
                translation_exists=os.path.exists(translated_path)
            )
            summary.append_file(doc)
                # en_file_path = os.path.join(en_repo_path, lang_file_relative_path)
                # lang_file_path = os.path.join(
                #     "docs", language_code, lang_file_relative_path
                # )

                # result = compare_commits(
                #     en_repo_path, lang_repo_path, en_file_path, lang_file_path
                # )
                # if result:
                #     outdated_files.append(result)
    print(summary)

if __name__ == "__main__":
    app()
