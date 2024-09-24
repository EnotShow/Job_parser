from src.cli import cli, add_cli_commands


def main():
    """Run administrative tasks."""
    add_cli_commands()
    cli()


if __name__ == "__main__":
    main()
