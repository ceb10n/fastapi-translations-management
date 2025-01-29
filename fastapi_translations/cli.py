from typing import Annotated

import typer
from rich.console import Console

from fastapi_translations import printer
from fastapi_translations.translations import Languages, Summary

console = Console()

app = typer.Typer(rich_markup_mode="rich")


@app.command("report")
def report(
    lang: Annotated[
        Languages,
        typer.Option(
            ...,
            "--language",
            "-l",
            help="The language to check for translations report",
        ),
    ],
    save_csv: Annotated[
        bool,
        typer.Option(
            "--csv",
            "-c",
            help="Save all missing and outdated translations to a csv file",
        ),
    ] = False,
) -> None:
    """Generate a report for the translated docs"""
    console.clear()
    summary = Summary(lang=lang.value)
    summary.generate()

    printer.print_table(summary, console, 10)

    if save_csv:
        printer.print_to_csv(summary)


def main() -> None:
    app()
