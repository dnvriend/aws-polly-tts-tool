"""Billing and pricing CLI commands."""

import sys

import click

from aws_polly_tts_tool.core.cost_explorer import get_polly_costs
from aws_polly_tts_tool.engines import list_all_engines


@click.command()
@click.option("--days", "-d", default=30, help="Number of days to query (default: 30)")
@click.option("--start-date", help="Custom start date (YYYY-MM-DD)")
@click.option("--end-date", help="Custom end date (YYYY-MM-DD)")
@click.option("--region", "-r", help="AWS region for Cost Explorer")
def billing(days: int, start_date: str | None, end_date: str | None, region: str | None) -> None:
    """
    Query AWS billing data for Polly usage.

    \b
    Examples:

    \b
        # Last 30 days of Polly costs
        aws-polly-tts-tool billing

    \b
        # Last 7 days
        aws-polly-tts-tool billing --days 7

    \b
        # Custom date range
        aws-polly-tts-tool billing --start-date 2025-01-01 --end-date 2025-01-31
    """
    try:
        click.echo("Querying AWS Cost Explorer...", err=True)
        costs = get_polly_costs(days=days, start_date=start_date, end_date=end_date, region=region)

        click.echo(f"\nPolly Costs ({costs['start_date']} to {costs['end_date']})")
        click.echo("=" * 60)
        click.echo(f"Total Cost: ${costs['total_cost']:.2f} {costs['currency']}")
        click.echo("\nBy Engine:")
        for engine, cost in costs["by_engine"].items():
            if cost > 0:
                click.echo(f"  {engine:12} ${cost:.2f}")

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@click.command()
def pricing() -> None:
    """
    Show Polly pricing information.

    \b
    Examples:

    \b
        # Display pricing table
        aws-polly-tts-tool pricing
    """
    engines = list_all_engines()

    click.echo("AWS Polly Pricing (Per 1 Million Characters)")
    click.echo("=" * 80)

    for engine_id, info in engines:
        click.echo(f"\n{info.name} Engine (${info.pricing_per_million:.2f}/1M characters)")
        click.echo(f"  Technology: {info.technology}")
        click.echo(f"  Quality: {info.quality}")
        click.echo(f"  Character Limit: {info.char_limit:,} chars per request")
        click.echo(f"  Concurrent Requests: {info.concurrent_requests}")
        if info.free_tier != "N/A":
            click.echo(f"  Free Tier: {info.free_tier}")
        click.echo(f"  Best For: {info.best_for}")

    click.echo("\n" + "=" * 80)
    click.echo("\nCost Examples:")
    click.echo("  1,000 words (~5,000 chars) with Standard:  $0.02")
    click.echo("  1,000 words (~5,000 chars) with Neural:    $0.08")
    click.echo("  50,000 word audiobook with Neural:         $4.00")
    click.echo("  50,000 word audiobook with Long-form:     $25.00")
