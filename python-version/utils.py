import json
from pathlib import Path

import typer


def get_config_path() -> Path:
    """
    Get the path to the configuration file.
    """
    users_home = Path.home()
    return users_home / ".config" / "acommit" / "config.json"


# TODO: Will have to look at this another time my retry logic is kinda fucked right now
def updated_github_token(config_path: Path):
    max_retries = 3
    retries = 0

    user_wants_to_add_token = typer.confirm(
        "Do you want to add your GitHub authentication token now?"
    )

    if not user_wants_to_add_token:
        typer.secho(
            "GitHub authentication token not added. You can add it later using the 'init' command.",
            fg=typer.colors.YELLOW,
        )
        return

    while retries < max_retries:
        if retries > 0:
            typer.secho(
                f"Attempt {retries + 1} of {max_retries}. Please try again.",
                fg=typer.colors.YELLOW,
            )

        try:
            github_token = typer.prompt(
                "Please enter your GitHub authentication token",
                hide_input=False,
                default=None,
            )

            if not github_token or github_token is None or github_token.strip() == "":
                raise ValueError("GitHub authentication token cannot be empty.")

            config_data = json.loads(config_path.read_text())
            config_data["githubAuthToken"] = github_token
            config_path.write_text(json.dumps(config_data, indent=2))

            typer.secho(
                "GitHub authentication token added successfully.",
                fg=typer.colors.GREEN,
            )
            return

        except ValueError as e:
            typer.secho(f"Error: {str(e)}", fg=typer.colors.RED)
            retries += 1
            typer.secho(f"Retry count: {retries}/{max_retries}", fg=typer.colors.CYAN)

        except (json.JSONDecodeError, OSError) as e:
            typer.secho(f"File error: {str(e)}", fg=typer.colors.RED)
            retries += 1
            typer.secho(f"Retry count: {retries}/{max_retries}", fg=typer.colors.CYAN)

        except KeyboardInterrupt:
            typer.secho("\nOperation cancelled by user.", fg=typer.colors.YELLOW)
            return

    # If we reach here, all retries were exhausted
    typer.secho(f"\n*** MAXIMUM RETRIES REACHED ***", fg=typer.colors.RED, bold=True)
    typer.secho(
        f"Failed to add GitHub token after {max_retries} attempts.",
        fg=typer.colors.RED,
    )
    typer.secho(
        "You can try again later using the 'init' command.",
        fg=typer.colors.YELLOW,
    )
