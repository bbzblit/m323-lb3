from datetime import date, datetime
from typing import Any
import pandas as pd
from .helper import time_to_string, remove_negative_delay
import csv
from typing import Iterable
from fpandas import FunctionalDF


def get_statistics_of_train(date: date, train: str):
    """
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
    """


def get_delay_of_exact_connection(date: date, train_line: str, time: str):
    df = FunctionalDF.from_csv(date)
    
    df = df.filter_content("LINIEN_TEXT", lambda x: x == train_line)
    fahrt_id = df.filter_content("ABFAHRTSZEIT", lambda x: x == time)[0]["FAHRT_ID"]
    df = df.filter_content("FAHRT_ID", lambda x: x == fahrt_id)
    stops = df["HALTESTELLEN_NAME"]
    df = remove_negative_delay(df)

    return {
        "Meta Informations": {
            "Train": train_line,
            "Start Time": time,
            "End Time": df["ANKUNFTSZEIT"][-1],
            "Stops": " -> ".join(stops),
        },
        "Delay Statistics": {
            "Minimum Delay": time_to_string(df["DELAY_ANKUFT"].min()),
            "Maximum Delay": time_to_string(df["DELAY_ANKUFT"].max()),
            "Average Delay": time_to_string(df["DELAY_ANKUFT"].mean()),
            "Median Delay": time_to_string(df["DELAY_ANKUFT"].median()),
        }
    }


"""
    delay_per_stop = {
        stops[0]: f"{time_to_string(df['DELAY_ABFAHRT'].iloc[0])} (Departure Delay)"
    }
    delay_per_stop.update(
        {
            stop: time_to_string(delay)
            for stop, delay in zip(stops[1:], df["DELAY_ANKUFT"].tolist()[1:])
        }
    )
"""


def get_statistics_of_day(date: date):
    df = FunctionalDF.from_csv(date)

    df = remove_negative_delay(df)

    delays = df["DELAY_ANKUFT"]
    maximum = delays.max()

    maximum = f"{time_to_string(maximum)} (Train: {', '.join(df.filter_content('DELAY_ANKUFT', lambda x: x == maximum)['LINIEN_TEXT'].tolist())})"
    return {
        "Meta Informations": {
            "Date": date,
        },
        "Delay Statistics": {
            "Minimum Delay": time_to_string(delays.min()),
            "Maximum Delay": maximum,
            "Average Delay": time_to_string(delays.mean()),
            "Median Delay": time_to_string(delays.median()),
        },
    }
