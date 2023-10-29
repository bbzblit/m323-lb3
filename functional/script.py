
import typer
from datetime import date, datetime
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print
from rich.table import Table
from InquirerPy import inquirer
from os.path import isfile, join
from os import listdir
import stats


def get_available_dates() -> list[date]:
    """
    Returns a list of available dates for which data is available.

    Returns:
        list[date]: A list of available dates.
    """
    files = filter(lambda f: isfile(join("./data", f)), listdir("./data"))
    return sorted({date.fromisoformat(f.removesuffix(".csv")) for f in files})


def get_train_line(date: date) -> str:
    """
    Prompts the user to select a train line for a given date.

    Args:
        date (date): The date for which to select a train line.

    Returns:
        str: The selected train line.
    """
    trains = stats.get_all_trains(date)
    return inquirer.fuzzy(
        message="Select the train line you want to look at",
        choices=trains,
    ).execute()


def get_start_time(date: date, train_line: str) -> datetime:
    """
    Prompts the user to select a start time for a given train line and date.

    Args:
        date (date): The date for which to select a start time.
        train_line (str): The train line for which to select a start time.

    Returns:
        datetime: The selected start time.
    """
    start_times = stats.get_start_times(date, train_line)

    selected_time = inquirer.select(
        message="Select the start time of the connection you want to look at",
        choices=map(lambda x: x[1], start_times),
    ).execute()

    for time in start_times:
        if time[1] == selected_time:
            return time[0]


def dict_to_table(table: Table, dictionary: dict) -> Table:
    """
    Converts a dictionary to a rich Table.

    Args:
        table (Table): The table to add the dictionary to.
        dictionary (dict): The dictionary to convert to a table.

    Returns:
        Table: The updated table.
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
    Prints a rich Table of statistics for a given train line.

    Args:
        statistics (dict): The statistics to print.
        train_line (str): The train line for which to print the statistics.

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
    Runs statistics for a given date and outputs the results to a table.

    Args:
        date (date): The date for which to run the statistics.

    Returns:
        None
    """
    statistics = stats.get_statistics_of_day(date)
    to_table(statistics, "All")


def run_delay_of_exact_connection(date: date):
    """
    Runs the delay of exact connection for a given date.

    Args:
        date (date): The date for which to run the delay of exact connection.

    Returns:
        None
    """
    train_line = get_train_line(date)
    time = get_start_time(date, train_line)
    delay = stats.get_delay_of_exact_connection(date, train_line, time)

    to_table(delay, train_line)


def run_statistic_of_train_line(date: date):
    """
    Runs statistics of a train line for a given date.

    Args:
        date (date): The date for which to run the statistics.

    Returns:
        None
    """
    train_line = get_train_line(date)
    statistics = stats.get_statistics_of_train(date, train_line)

    to_table(statistics, train_line)


def main():
    """
    This function allows the user to select a date and a task to run. The available dates are obtained by calling the
    get_available_dates() function. The user is prompted to select a date from the available dates, and then to select
    a task to run from a list of three options. Depending on the selected task, one of three functions is called:
    run_statistic_of_day(), run_delay_of_exact_connection(), or run_statistic_of_train_line(). If the selected task
    is not recognized, an error message is printed.
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
        ],
    ).execute()

    if task == "Statistic of Day":
        run_statistic_of_day(date)
    elif task == "Delay of exact connection":
        run_delay_of_exact_connection(date)
    elif task == "Statistic of Train Line":
        run_statistic_of_train_line(date)
    else:
        print(
            "[red]Internal programm error[/red] - Task not found\nPlease open an issue on [link=https://github.com/bbzblit/m323-lb3]GitHub[/link]"
        )


if __name__ == "__main__":
    typer.run(main)
