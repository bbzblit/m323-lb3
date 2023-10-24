"""
An imperative script to run different tasks on the data.
The data is loaded from the `./data` folder.
The data is real life data from the SBB which contains the expected departure and the real departure of trains.
"""

from datetime import date, datetime
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print
from rich.table import Table
from InquirerPy import inquirer
from os.path import isfile, join
from os import listdir
from dotenv import load_dotenv, find_dotenv

import typer
import stats


def get_available_dates() -> list[date]:
    """
    Returns a list of available dates for which data is available.

    Returns:
        list[date]: A list of dates for which data is available.
    """
    files = [f for f in listdir("./data") if isfile(join("./data", f))]
    return sorted({date.fromisoformat(f.removesuffix(".csv")) for f in files})


def get_train_line(date: date) -> str:
    """
    Asks the user to select a train line from a list of available train lines for a given date.

    Args:
        date (date): The date for which to get the available train lines.

    Returns:
        str: The name of the selected train line.
    """
    trains = stats.get_all_trains(date)
    return inquirer.fuzzy(
        message="Select the train line you want to look at",
        choices=trains,
    ).execute()


def get_start_time(date: date, train_line: str) -> datetime:
    """
    Asks the user to select a start time for a given train line and date.

    Args:
        date (date): The date for which to get the start times.
        train_line (str): The name of the train line for which to get the start times.

    Returns:
        datetime: The selected start time.
    """
    start_times = stats.get_start_times(date, train_line)

    selected_time = inquirer.select(
        message="Select the start time of the connection you want to look at",
        choices=[choice[1] for choice in start_times],
    ).execute()

    for time in start_times:
        if time[1] == selected_time:
            return time[0]


def dict_to_table(table: Table, dictionary: dict) -> Table:
    """
    Converts a dictionary to a rich Table object.

    Args:
        table (rich.table.Table): The table object to add rows to.
        dictionary (dict): The dictionary to convert to a table.

    Returns:
        rich.table.Table: The table object with the dictionary data added.
    """
    for key, value in dictionary.items():
        if isinstance(value, dict):
            table.add_row(f"[bold][bright_magenta]{key}[/bold][/bright_magenta]")
            dict_to_table(table, value)
        else:
            table.add_row(key, ", ".join(v for v in value if isinstance(v, str)) if isinstance(value, list) else str(value))
    table.add_section()
    return table

def to_table(statistics: dict, train_line: str):
    """
    Converts a dictionary of statistics into a table and prints it to the console.

    Args:
        statistics (dict): A dictionary containing statistics for a train line.
        train_line (str): The name of the train line.

    Returns:
        None
    """
    table = Table(
        title=f"Delay of Train Line [bold]{train_line}[/bold]",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Statistic")
    table.add_column("Value")

    dict_to_table(table, statistics)

    print(table)


def run_statistic_of_day(date: date):
    """
    Runs the statistic of the day for a given date.

    Args:
        date (date): The date for which to run the statistic.

    Returns:
        None
    """
    statistics = stats.get_statistics_of_day(date)
    to_table(statistics, "All")


def run_delay_of_exact_connection(date: date):
    """
    Runs the delay of an exact connection for a given date.

    Args:
        date (date): The date for which to run the delay.

    Returns:
        None
    """
    train_line = get_train_line(date)
    time = get_start_time(date, train_line)
    delay = stats.get_delay_of_exact_connection(date, train_line, time)

    to_table(delay, train_line)


def run_statistic_of_train_line(date: date):
    """
    Runs the statistic of a train line for a given date.

    Args:
        date (date): The date for which to run the statistic.

    Returns:
        None
    """
    train_line = get_train_line(date)
    statistics = stats.get_statistics_of_train(date, train_line)

    to_table(statistics, train_line)

def run_chat_with_ai(date: date):
    """
    Runs a chat with an AI for a given date.

    Args:
        date (date): The date for which to run the chat.

    Returns:
        None
    """
    question = inquirer.text(message="What do you want to ask the AI?").execute()
    answer = stats.ask_ai(question, date)

    print(f"[bold]Answer:[/bold] {answer}")


def main():
    """
    The main function that runs the script.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Indexing Data...")
        available_dates = get_available_dates()

    date = inquirer.select(
        message="Select the date you want to look at",
        choices=[date for date in available_dates],
    ).execute()

    task = inquirer.select(
        message="Select the task you want to run",
        choices=[
            "Statistic of Day",
            "Delay of exact connection",
            "Statistic of Train Line",
            "Chat with AI"
        ],
    ).execute()

    if task == "Statistic of Day":
        run_statistic_of_day(date)
    elif task == "Delay of exact connection":
        run_delay_of_exact_connection(date)
    elif task == "Statistic of Train Line":
        run_statistic_of_train_line(date)
    elif task == "Chat with AI":
        run_chat_with_ai(date)
    else:
        print(
            "[red]Internal programm error[/red] - Task not found\nPlease open an issue on [link=https://github.com/bbzblit/m323-lb3]GitHub[/link]"
        )


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    typer.run(main)
