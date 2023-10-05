from datetime import date, datetime
import pandas as pd
from .helper import time_to_string


def get_statistics_of_train(date: date, train: str):
    df = pd.read_csv(f"./data/{date.isoformat()}.csv")

    df = df[df["LINIEN_TEXT"] == train]
    df = df[df["DELAY_ABFAHRT"].isna()]

    df.loc[df["DELAY_ANKUFT"] < 0, "DELAY_ANKUFT"] = 0

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
    df = pd.read_csv(f"./data/{date.isoformat()}.csv")

    df = df[df["LINIEN_TEXT"] == train_line]
    fahrt_id = df[df["ABFAHRTSZEIT"] == time].iloc[0]["FAHRT_ID"]
    df = df[df["FAHRT_ID"] == fahrt_id]
    stops = df["HALTESTELLEN_NAME"].unique().tolist()

    df.loc[df["DELAY_ANKUFT"] < 0, "DELAY_ANKUFT"] = 0
    df.loc[df["DELAY_ABFAHRT"] < 0, "DELAY_ABFAHRT"] = 0

    return {
        "Meta Informations": {
            "Train": train_line,
            "Time": time,
            "Stops": " -> ".join(stops),
        },
        "Delay Statistics": {
            "Minimum Delay": time_to_string(df["DELAY_ANKUFT"].min()),
            "Maximum Delay": time_to_string(df["DELAY_ANKUFT"].max()),
            "Average Delay": time_to_string(df["DELAY_ANKUFT"].mean()),
            "Median Delay": time_to_string(df["DELAY_ANKUFT"].median()),
        },
        "Delay per Stop": {
            stop: time_to_string(delay)
            for stop, delay in zip(stops[1:], df["DELAY_ANKUFT"].tolist()[1:])
        },
    }


def get_statistics_of_day(date: date):
    df = pd.read_csv(f"./data/{date.isoformat()}.csv")

    df.loc[df["DELAY_ANKUFT"] < 0, "DELAY_ANKUFT"] = 0
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
