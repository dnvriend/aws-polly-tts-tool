"""Voice listing CLI commands."""

import sys

import click

from aws_polly_tts_tool.core import get_polly_client
from aws_polly_tts_tool.utils import format_table_row
from aws_polly_tts_tool.voices import VoiceManager


@click.command(name="list-voices")
@click.option("--engine", "-e", help="Filter by engine (standard, neural, generative, long-form)")
@click.option("--language", "-l", help="Filter by language code (e.g., en-US, es-ES)")
@click.option("--gender", "-g", help="Filter by gender (Female, Male)")
@click.option("--region", "-r", help="AWS region (default: from AWS config)")
def list_voices(
    engine: str | None, language: str | None, gender: str | None, region: str | None
) -> None:
    """
    List all available Polly voices.

    \b
    Examples:

    \b
        # List all voices
        aws-polly-tts-tool list-voices

    \b
        # Filter by engine
        aws-polly-tts-tool list-voices --engine neural

    \b
        # Filter by language
        aws-polly-tts-tool list-voices --language en-US

    \b
        # Combine filters
        aws-polly-tts-tool list-voices --engine neural --language en --gender Female

    \b
        # Use with grep for searching
        aws-polly-tts-tool list-voices | grep British
    """
    try:
        client = get_polly_client(region)
        voice_manager = VoiceManager(client)
        voices = voice_manager.list_voices(engine=engine, language=language, gender=gender)

        if not voices:
            click.echo("No voices found matching filters.", err=True)
            sys.exit(1)

        # Print header
        widths = [15, 10, 12, 20, 40]
        click.echo(
            format_table_row(["Voice", "Gender", "Language", "Engines", "Description"], widths)
        )
        click.echo("=" * sum(widths))

        # Print voices
        for name, profile in voices:
            engines_str = ", ".join(profile.supported_engines)
            desc = (
                profile.description[:37] + "..."
                if len(profile.description) > 40
                else profile.description
            )
            click.echo(
                format_table_row(
                    [profile.name, profile.gender, profile.language_code, engines_str, desc], widths
                )
            )

        click.echo(f"\nTotal: {len(voices)} voices")

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
