import pandas as pd
from pandas import DataFrame
from datetime import date


def time_to_string(value: int) -> str:
    """
    Converts a time value in seconds to a string representation.

    Args:
        value (int): The time value in seconds.

    Returns:
        str: The string representation of the time value.
    """

    if value % 60 == 0:
        if value == 0:
            return "No Delay"
        if value < 120:
            return f"[bright_yellow]{round(value // 60)} min[/bright_yellow]"
        elif value < 300:
            return f"[orange_red1]{round(value // 60)} min[/orange_red1]"
        return f"[bright_red]{round(value // 60)} min[/bright_red]"

    elif value < 60:
        return f"{round(value)} sec"

    if value < 120:
        return f"[bright_yellow]{round(value // 60)} min {round(value % 60)} sec[/bright_yellow]"
    elif value < 300:
        return f"[orange_red1]{round(value // 60)} min {round(value % 60)} sec[/orange_red1]"
    return f"[bright_red]{round(value // 60)} min {round(value % 60)} sec[/bright_red]"


def from_csv(date: date) -> DataFrame:
    return pd.read_csv(f"./data/{date.isoformat()}.csv")
