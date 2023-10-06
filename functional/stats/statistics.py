from datetime import date, datetime
from typing import Any
import pandas as pd
from .helper import time_to_string
import csv
from typing import Iterable
import re

class FunctionalSeries:
    
    dtype = str
    serie = []

    def __init__(self, it: Iterable) -> None:
        self.serie = list(it)

    def _to_int(self):
        if self.dtype != float:
            self.serie = list(map(float, self))
            self.dtype = float
        
    def __getitem__(self, __name: int) -> Any:
        return self.serie[__name]
    
    def __str__(self) -> str:
        return str(self.serie)

    def mean(self):
        self._to_int()
        return sum(self.serie) / len(self.serie)
    
    def median(self):
        self._to_int()
        return sorted(self.serie)[len(self.serie) // 2]
    
    def min(self):
        self._to_int()
        return min(self.serie)
    
    def max(self):
        self._to_int()
        return max(self.serie)


class FunctionalDF:
    content = {}

    def __init__(self, content) -> None:
        if content:
            self.content = content

    def __getitem__(self, __name: int | str) -> dict[str, str] | FunctionalSeries:
        if isinstance(__name, str):
            return FunctionalSeries(self.content[__name])
        return {k: v[__name] for k, v in self.content.items()}

    def to_int(self, key: str) -> "FunctionalDF":
        return FunctionalDF(
            {
                k: [int(v) if v != "" else 0 for v in value]
                if k == key
                else value
                for k, value in self.content.items()
            }
        )

    def filter_content(self, key: str, expression) -> "FunctionalDF":
        indexes = [i for i, x in enumerate(self.content[key]) if expression(x)]
        return FunctionalDF(
            {k: [v[i] for i in indexes] for k, v in self.content.items()}
        )

    def query_update(self, key: str, expression, new_value: Any) -> "FunctionalDF":
        indexes = [i for i, x in enumerate(self.content[key]) if expression(x)]
        return FunctionalDF(
            {
                key: [new_value if i in indexes else v for i, v in enumerate(value)]
                if key == key
                else value
                for key, value in self.content.items()
            }
        )

    @staticmethod
    def from_csv(date: date) -> "FunctionalDF":
        with open(f"./data/{date.isoformat()}.csv", "r") as file:
            reader = csv.DictReader(file)
            content = dict(
                zip(
                    (i for i in reader.fieldnames),
                    zip(*[row.values() for row in reader]),
                )
            )
        return FunctionalDF(content)


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
    df = df.query_update("DELAY_ANKUFT", lambda x: re.match(r"^(-\d+(.\d+)?|)$", x), 0)

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
    df = pd.read_csv(f"./data/{date.isoformat()}.csv")

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
