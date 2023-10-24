from datetime import date, datetime
from pandas import DataFrame
import pandas as pd
from .helper import time_to_string, from_csv


def _remove_negative_delays(df: DataFrame) -> DataFrame:
    """
    Removes negative delays from a DataFrame containing arrival and departure delays.

    Args:
        df (pandas.DataFrame): The DataFrame containing the arrival and departure delays.

    Returns:
        pandas.DataFrame: The DataFrame with negative delays set to 0.
    """
    df.loc[df["DELAY_ANKUFT"] < 0, "DELAY_ANKUFT"] = 0
    df.loc[df["DELAY_ABFAHRT"] < 0, "DELAY_ABFAHRT"] = 0
    return df



def get_statistics_of_train(date: date, train: str):
    """
    Returns statistics for a given train on a given date.

    Args:
        date (date): The date to get statistics for.
        train (str): The name of the train to get statistics for.

    Returns:
        dict: A dictionary containing meta information about the train and delay statistics.

    """
    df = from_csv(date)

    df = df[df["LINIEN_TEXT"] == train]
    df = df[df["DELAY_ABFAHRT"].isna()]

    df = _remove_negative_delays(df)

    stops = df["HALTESTELLEN_NAME"].unique().tolist()

    return {
        "Meta Informations": {
            "Rides": len(df),
            "Train": train,
            "Date": date,
            "Endstations": stops,
        },
        "Delay Statistics": {
            "Minimum Delay": time_to_string(df["DELAY_ANKUFT"].min()),
            "Maximum Delay": time_to_string(df["DELAY_ANKUFT"].max()),
            "Average Delay": time_to_string(df["DELAY_ANKUFT"].mean()),
            "Median Delay": time_to_string(df["DELAY_ANKUFT"].median()),
        },
    }


def get_delay_of_exact_connection(date: date, train_line: str, time: str):
    """
    Returns delay statistics for a specific train line at a specific time.

    Args:
        date (date): The date of the train schedule.
        train_line (str): The name of the train line.
        time (str): The departure time of the train.

    Returns:
        dict: A dictionary containing the following keys:
            - "Meta Informations": A dictionary containing meta information about the train line and stops.
            - "Delay Statistics": A dictionary containing delay statistics for the train line.
            - "Delay per Stop": A dictionary containing delay information for each stop on the train line.
    """

    df = from_csv(date)

    df = df[df["LINIEN_TEXT"] == train_line]
    fahrt_id = df[df["ABFAHRTSZEIT"] == time].iloc[0]["FAHRT_ID"]
    df = df[df["FAHRT_ID"] == fahrt_id]
    stops = df["HALTESTELLEN_NAME"].unique().tolist()

    df = _remove_negative_delays(df)

    delay_per_stop = {
        stops[0]: f"{time_to_string(df['DELAY_ABFAHRT'].iloc[0])}"
    }
    delay_per_stop.update(
        {
            stop: time_to_string(delay)
            for stop, delay in zip(stops[1:], df["DELAY_ANKUFT"].tolist()[1:])
        }
    )

    return {
        "Meta Informations": {
            "Train": train_line,
            "Start Time": time,
            "End Time": df["ANKUNFTSZEIT"].iloc[-1],
            "Stops": " -> ".join(stops),
        },
        "Delay Statistics": {
            "Minimum Delay": time_to_string(df["DELAY_ANKUFT"].min()),
            "Maximum Delay": time_to_string(df["DELAY_ANKUFT"].max()),
            "Average Delay": time_to_string(df["DELAY_ANKUFT"].mean()),
            "Median Delay": time_to_string(df["DELAY_ANKUFT"].median()),
        },
        "Delay per Stop": delay_per_stop,
    }


def get_statistics_of_day(date: date):
    """
    Returns a dictionary containing delay statistics for a given date.

    Args:
        date (date): The date for which to retrieve delay statistics.

    Returns:
        dict: A dictionary containing delay statistics for the given date.
            The dictionary has two keys:
                - "Meta Informations": A dictionary containing meta information about the statistics.
                    - "Date": The date for which the statistics were retrieved.
                - "Delay Statistics": A dictionary containing delay statistics.
                    - "Minimum Delay": The minimum delay in string format.
                    - "Maximum Delay": The maximum delay in string format, along with the train(s) responsible for the delay.
                    - "Average Delay": The average delay in string format.
                    - "Median Delay": The median delay in string format.
    """
    df = from_csv(date)
    df = _remove_negative_delays(df)

    maximum = df["DELAY_ANKUFT"].max()
    maximum = f"{time_to_string(maximum)} (Train: {', '.join(df[df['DELAY_ANKUFT'] == maximum]['LINIEN_TEXT'].tolist())})"

    return {
        "Meta Informations": {
            "Date": date,
        },
        "Delay Statistics": {
            "Minimum Delay": time_to_string(df["DELAY_ANKUFT"].min()),
            "Maximum Delay": maximum,
            "Average Delay": time_to_string(df["DELAY_ANKUFT"].mean()),
            "Median Delay": time_to_string(df["DELAY_ANKUFT"].median()),
        },
    }
