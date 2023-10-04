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
    files = [f for f in listdir("./data") if isfile(join("./data", f))]
    return {date.fromisoformat(f.removesuffix(".csv")) for f in files}


def get_train_line(date: date) -> str:
    trains = stats.get_all_trains(date)
    return inquirer.fuzzy(
        message="Select the train line you want to look at",
        choices=trains,
    ).execute()


def get_start_time(date: date, train_line: str) -> datetime:
    start_times = stats.get_start_times(date, train_line)

    selected_time = inquirer.select(
        message="Select the start time of the connection you want to look at",
        choices=[choice[1] for choice in start_times],
    ).execute()

    for time in start_times:
        if time[1] == selected_time:
            return time[0]


def dict_to_table(table: Table, dictionary: dict) -> Table:
    for key, value in dictionary.items():
        if isinstance(value, dict):
            dict_to_table(table, value)
            table.add_section()
        else:
            table.add_row(key, ", ".join(v for v in value if isinstance(v, str)) if isinstance(value, list) else str(value))
    table.add_section()
    return table


def to_table(statistics: dict, train_line: str):
    table = Table(
        title=f"Delay of Train Line [bold]{train_line}[/bold]",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Statistic")
    table.add_column("Value")

    dict_to_table(table, statistics["meta"])
    del statistics["meta"]

    for key, value in statistics.items():
        if value % 60 == 0:
            table.add_row(key, f"{round(value // 60)} min")
        else:
            table.add_row(key, f"{round(value // 60)} min {round(value % 60)} sec")
    print(table)


def run_statistic_of_day(date: date):
    pass


def run_delay_of_exact_connection(date: date):
    train_line = get_train_line(date)
    time = get_start_time(date, train_line)
    delay = stats.get_delay_of_exact_connection(date, train_line, time)

    to_table(delay, train_line)


def run_statistic_of_train_line(date: date):
    train_line = get_train_line(date)
    statistics = stats.get_statistics_of_train(date, train_line)

    to_table(statistics, train_line)


def main():
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
