import re

from rich.columns import Columns
from rich.console import Console
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress
from rich.table import Table

console = Console()


def print_markdown(text) -> None:
    """Prints a rich info message. Support Markdown syntax."""

    md = Padding(Markdown(text), 2)
    console.print(md)


def print_step(text) -> None:
    """Prints a rich info message."""

    panel = Panel(Text(text, justify="left"))
    console.print(panel)

def print_start(text) -> None:
    """Prints a rich colored info message without the panelling."""
    formatted_text = "\n[green][+][/green] " + text + "[white]:[/white]"
    console.print(formatted_text)

def print_substep(text) -> None:
    """Prints a rich colored info message without the panelling."""
    formatted_text = "[blue][*][/blue] " + text + " [white]...[/white]"
    console.print(formatted_text)

def print_finished(text) -> None:
    """Prints a rich colored info message without the panelling."""
    formatted_text = "[green][+] " + text + "!\n"
    console.print(formatted_text)

def print_table(items) -> None:
    """Prints items in a table."""

    console.print(Columns([Panel(f"[blue]{item}", expand=True) for item in items]))

def print_error(text) -> None:
    """Prints a rich colored error message without the panelling."""
    formatted_text = "[red][!][/red] " + text + "[red]![/red]\n"
    console.print(formatted_text)

def display_post_score(title, score) -> None:
    """Displays a visual representation of the post score."""
    console = Console()

    # Normalize the score to fit within the column
    normalized_score = min(max(score, 0), 100)

    # Create a table to represent the information
    table = Table()
    table.add_column("Post", justify="left", style="cyan")
    table.add_column("Score", justify="left", style="green")

    # Create a bar graph based on the normalized score
    bar_length = int((normalized_score / 100) * 20)
    bar_graph = "[green][{}{}] [/green]".format("=" * bar_length, " " * (20 - bar_length))

    # Add rows to the table
    table.add_row(title, f"[bold cyan]{score}[/bold cyan]")
    table.add_row("", bar_graph)

    console.print(table)


def handle_input(
    message: str = "",
    check_type=False,
    match: str = "",
    err_message: str = "",
    nmin=None,
    nmax=None,
    oob_error="",
    extra_info="",
    options: list = None,
    default=NotImplemented,
    optional=False,
):
    if optional:
        console.print(message + "\n[green]This is an optional value. Do you want to skip it? (y/n)")
        if input().casefold().startswith("y"):
            return default if default is not NotImplemented else ""
    
    if options is None:
        match = re.compile(match)
        console.print("[green bold]" + extra_info, no_wrap=True)
        while True:
            console.print(message, end="")
            user_input = input("").strip()
            if check_type is not False:
                try:
                    user_input = check_type(user_input)
                    if (nmin is not None and user_input < nmin) or (
                        nmax is not None and user_input > nmax
                    ):
                        # FAILSTATE Input out of bounds
                        console.print("[red]" + oob_error)
                        continue
                    break  # Successful type conversion and number in bounds
                except ValueError:
                    # Type conversion failed
                    console.print("[red]" + err_message)
                    continue
            elif match != "" and re.match(match, user_input) is None:
                console.print("[red]" + err_message + "\nAre you absolutely sure it's correct?(y/n)")
                if input().casefold().startswith("y"):
                    break
                continue
            else:
                # FAILSTATE Input STRING out of bounds
                if (nmin is not None and len(user_input) < nmin) or (
                    nmax is not None and len(user_input) > nmax
                ):
                    console.print("[red bold]" + oob_error)
                    continue
                break  # SUCCESS Input STRING in bounds
        return user_input
    
    console.print(extra_info, no_wrap=True)
    while True:
        console.print(message, end="")
        user_input = input("").strip()
        if check_type is not False:
            try:
                isinstance(eval(user_input), check_type)
                return check_type(user_input)
            except:
                console.print(
                    "[red bold]"
                    + err_message
                    + "\nValid options are: "
                    + ", ".join(map(str, options))
                    + "."
                )
                continue
        if user_input in options:
            return user_input
        console.print(
            "[red bold]" + err_message + "\nValid options are: " + ", ".join(map(str, options)) + "."
        )
