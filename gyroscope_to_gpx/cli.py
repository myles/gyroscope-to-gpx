from pathlib import Path

import click

from .service import gyroscope_to_gpx


@click.command()
@click.version_option()
@click.option(
    "--visits",
    "-v",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
    required=True,
    help="Path to the Gyroscope visits data export file",
)
@click.option(
    "--travels",
    "-t",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
    required=True,
    help="Path to the Gyroscope travels data export file",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(writable=True, resolve_path=True),
    required=True,
    help="Path to the output the GPX file",
)
def cli(visits, travels, output):
    visits_csv_path = Path(visits)
    travels_csv_path = Path(travels)
    output_gpx_path = Path(output)

    gyroscope_to_gpx(visits_csv_path, travels_csv_path, output_gpx_path)
