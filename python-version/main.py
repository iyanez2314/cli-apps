import json
import os
from pathlib import Path

import typer
from rich import print_json

from utils import get_config_path, updated_github_token, write_json_dump

app = typer.Typer()


@app.command()
def init():
    """
    Initialize the config file in ~/.config/acommit.
    """

    config_path = get_config_path()

    if not config_path.parent.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)

    if not config_path.exists():
        try:
            write_json_dump(config_path)
            typer.secho(f"Config file created at {config_path}", fg=typer.colors.GREEN)
        except Exception as e:
            typer.secho(f"Error creating config file: {e}", fg=typer.colors.RED)
            return
        typer.secho(f"Config file created at {config_path}", fg=typer.colors.GREEN)
    else:
        overwrite = typer.confirm(
            f"Config file already exists at {config_path}. Do you want to overwrite it?"
        )
        if overwrite:
            try:
                write_json_dump(config_path)
                typer.secho(
                    f"Config file overwritten at {config_path}", fg=typer.colors.GREEN
                )
            except Exception as e:
                typer.secho(f"Error overwriting config file: {e}", fg=typer.colors.RED)
                return
        else:
            typer.secho("Config file not modified.", fg=typer.colors.YELLOW)


@app.command()
def showconfig():
    """
    Show your current CLI configuration.
    """
    config_path = get_config_path()
    if not config_path.exists():
        typer.secho(f"No config file found at {config_path}", fg=typer.colors.RED)
        return

    try:
        config_data = json.loads(config_path.read_text())
        print_json(json.dumps(config_data, indent=2))
    except json.JSONDecodeError as e:
        typer.secho(f"Error reading config file: {e}", fg=typer.colors.RED)


if __name__ == "__main__":
    app()
