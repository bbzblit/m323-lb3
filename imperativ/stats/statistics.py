from datetime import date, datetime
from pandas import DataFrame
import pandas as pd
from .helper import time_to_string


def _remove_negative_delays(df: DataFrame) -> DataFrame:
    df.loc[df["DELAY_ANKUFT"] < 0, "DELAY_ANKUFT"] = 0
    df.loc[df["DELAY_ABFAHRT"] < 0, "DELAY_ABFAHRT"] = 0
    return df


def _from_csv(date: date) -> DataFrame:
    return pd.read_csv(f"./data/{date.isoformat()}.csv")


def get_statistics_of_train(date: date, train: str):
    df = _from_csv(date)

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
    df = _from_csv(date)

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
    df = _from_csv(date)
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
