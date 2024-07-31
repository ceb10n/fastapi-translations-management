import datetime

from fastapi_translations.models import DocFile, Summary


def test_must_compute_summary_when_adding_docfile():
    doc1 = DocFile(
        translation_lang="es",
        original_file="/test/file1.md",
        original_commit=datetime.datetime(2024, 1, 1, 0, 0, 0),
        translation_file="/test/file1.md",
        translation_exists=True,
        translation_commit=datetime.datetime(2024, 1, 15, 0, 0, 0),
        translation_is_outdated=True
    )
    doc2 = DocFile(
        translation_lang="es",
        original_file="/test/file2.md",
        original_commit=datetime.datetime(2024, 1, 1, 0, 0, 0),
        translation_file="/test/file2.md",
        translation_exists=True,
        translation_commit=datetime.datetime(2024, 1, 1, 0, 0, 0),
        translation_is_outdated=False
    )
    doc3 = DocFile(
        translation_lang="es",
        original_file="/test/file3.md",
        original_commit=datetime.datetime(2024, 1, 1, 0, 0, 0),
        translation_file=None,
        translation_exists=False,
        translation_commit=None,
        translation_is_outdated=False
    )
    summary = Summary(lang="es")
    summary.append_file(doc1)
    summary.append_file(doc2)
    summary.append_file(doc3)

    assert summary.files_analyzed == 3
    assert summary.files_missing_translation == 1
    assert summary.files_outdated == 1
    assert summary.files_translated == 2
