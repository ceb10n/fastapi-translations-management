import csv

from rich.console import Console
from rich.table import Table

from fastapi_translations.translations import Document, Summary


def print_table(
    summary: Summary, console: Console, table_size: int = 10
) -> None:
    console.clear()

    table_stats = Table(title="Stats")
    table_stats.add_column("📂 FastAPI docs")
    _create_missing_translations_header(table_stats, summary)
    table_stats.add_column("📅 Oudated translations")

    table_docs = Table()
    table_docs.add_column("Count")
    table_docs.add_row(f"{summary.files_analyzed}")

    table_missing = _create_missing_translations_table(summary)

    table_outdated = Table()
    table_outdated.add_column("Count", justify="center", style="bold cyan")
    table_outdated.add_column("Percentage", justify="center", style="bold cyan")

    table_outdated.add_row(
        f"{summary.files_outdated}",
        f"% {summary.percentage_outdated_translation:.2f}",
    )

    table_stats.add_row(table_docs, table_missing, table_outdated)
    console.print(table_stats)
    console.line()

    table_files = Table(title="🆘 Need help on")
    need_help_tables = []

    if summary.percentage_missing_translation > 0.0:
        table_files.add_column(f"First {table_size} missing translations")

        table_first_missing = Table()
        table_first_missing.add_column(
            "📂 File", justify="left", style="bold cyan"
        )

        for file in summary.first_missing_translation_files(table_size):
            table_first_missing.add_row(f"📂 {file.original_file}")

        need_help_tables.append(table_first_missing)

    table_files.add_column(f"First {table_size} outdated documents")

    table_first_outdated = Table()
    table_first_outdated.add_column(
        "📂 File", justify="left", style="bold cyan"
    )

    for file in summary.first_outdated_files(table_size):
        table_first_outdated.add_row(f"📂 {file.original_file}")

    need_help_tables.append(table_first_outdated)

    table_files.add_row(*need_help_tables)
    console.print(table_files)


def print_to_csv(summary: Summary) -> None:
    header = Document.model_fields.keys()
    with open(
        f"fastapi-translations-lang-{summary.lang}.csv", "w", newline=""
    ) as f:
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        writer.writerows([f.model_dump() for f in summary.files])


def _create_missing_translations_header(table: Table, summary: Summary) -> None:
    if summary.percentage_missing_translation == 0:
        table.add_column("🎉 No missing translations", justify="center")

    elif summary.percentage_missing_translation < 10.0:
        table.add_column("😃 Missing translations", justify="center")

    elif summary.percentage_missing_translation < 50.0:
        table.add_column("😐 Missing translations", justify="center")

    else:
        table.add_column("😢 Missing translations", justify="center")


def _create_missing_translations_table(summary: Summary) -> Table:
    table_missing = Table()

    if summary.percentage_missing_translation == 0:
        table_missing.add_column(
            "🎇 Congratulations", justify="center", style="bold cyan"
        )
        table_missing.add_row("All documents are translated!")
        table_missing.add_row("Have an 🍦 ice cream now, you deserve it! 🤗")

    else:
        table_missing.add_column("Count", justify="center", style="bold cyan")
        table_missing.add_column(
            "Percentage", justify="center", style="bold cyan"
        )
        table_missing.add_row(
            f"{summary.files_missing_translation}",
            f"% {summary.percentage_missing_translation:.2f}",
        )

    return table_missing
