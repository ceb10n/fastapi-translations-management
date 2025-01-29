import datetime

from fastapi_translations.translations import Document, Summary


def test_must_compute_summary_when_adding_document():
    doc1 = Document(
        translation_lang="es",
        original_file="/test/file1.md",
        translation_file="/test/file1.md",
        translation_exists=True,
        original_commit=datetime.datetime(2024, 1, 1, 0, 0, 0),
        translation_commit=datetime.datetime(2024, 1, 15, 0, 0, 0),
    )
    doc2 = Document(
        translation_lang="es",
        original_file="/test/file2.md",
        translation_file="/test/file2.md",
        translation_exists=True,
        original_commit=datetime.datetime(2024, 1, 2, 0, 0, 0),
        translation_commit=datetime.datetime(2024, 1, 1, 0, 0, 0),
    )
    doc3 = Document(
        translation_lang="es",
        original_file="/test/file3.md",
        original_commit=datetime.datetime(2024, 1, 1, 0, 0, 0),
        translation_file=None,
        translation_exists=False,
        translation_commit=None,
    )
    summary = Summary(lang="es")
    summary.append_document(doc1)
    summary.append_document(doc2)
    summary.append_document(doc3)

    assert summary.files_analyzed == 3
    assert summary.files_missing_translation == 1
    assert summary.files_outdated == 1
    assert summary.files_translated == 2
