"""CLI entry point for aws-polly-tts-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from aws_polly_tts_tool.utils import get_greeting


@click.command()
@click.version_option(version="0.1.0")
def main() -> None:
    """A CLI that provides TTS using Amazon Polly"""
    click.echo(get_greeting())


if __name__ == "__main__":
    main()
