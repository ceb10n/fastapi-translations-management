import datetime

from fastapi_translations.translations import Document


def test_translation_is_outdated_should_return_true_if_english_document_has_older_commit_than_the_translated_document():
    document = Document(
        translation_lang="es",
        original_file="/test/file1.md",
        translation_file="/test/file1.md",
        translation_exists=True,
        original_commit=datetime.datetime(2025, 1, 28, 0, 0, 0),
        translation_commit=datetime.datetime(2025, 1, 29, 0, 0, 0),
    )

    assert not document.translation_is_outdated
