from typing import Any, Iterable
from datetime import date

from .series import FunctionalSeries

import csv

class FunctionalDF:
    content = {}

    def __init__(self, content) -> None:
        if content:
            self.content = content

    def __getitem__(self, key: int | str) -> dict[str, str] | FunctionalSeries:
        if isinstance(key, str):
            return FunctionalSeries(self.content[key])
        return {k: v[key] for k, v in self.content.items()}

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
    
    def cast(self, key: str, dtype: type, default) -> "FunctionalDF":
        return FunctionalDF(
            {
                k: [dtype(v) if v != "" else default for v in value]
                if k == key
                else value
                for k, value in self.content.items()
            }
        )
    
    def iterrows(self) -> Iterable[dict[str, str]]:
        return (dict(zip(self.content.keys(), t)) for t in zip(*self.content.values()))

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


