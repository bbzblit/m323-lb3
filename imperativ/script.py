import typer
from datetime import date
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print
from InquirerPy import inquirer
from os.path import isfile, join
from os import listdir
import stats

def get_available_dates() -> list[date]:
    files = [f for f in listdir("./data") if isfile(join("./data", f))]
    return {date.fromisoformat(f.removesuffix(".csv")) for f in files}

def get_train_line(date: date) -> str:
    trains = stats.get_all_trains(date)
    return inquirer.select(
        message="Select the train line you want to look at",
        choices=trains,
    ).execute()


def run_statistic_of_day(date: date):
    pass

def run_delay_of_exact_connection(date: date):
    train_line = get_train_line(date)
    

def run_statistic_of_train_line(date: date):
    train_line = get_train_line(date)

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
        choices=["Statistic of Day", "Delay of exact connection", "Statistic of Train Line"],
    ).execute()
    
    if task == "Statistic of Day":
        run_statistic_of_day(date)
    elif task == "Delay of exact connection":
        run_delay_of_exact_connection(date)
    elif task == "Statistic of Train Line":
        run_statistic_of_train_line(date)
    else:
        print("[red]Internal programm error[/red] - Task not found\nPlease open an issue on [link=https://github.com/bbzblit/m323-lb3]GitHub[/link]")

if __name__ == "__main__":
    typer.run(main)
