from typing import Any, Iterable
from datetime import date

from .series import FunctionalSeries

import csv

class FunctionalDF:
    """
    A functional-style implementation of a DataFrame.

    This class provides a way to manipulate tabular data in a functional way, using methods like `filter_content`,
    `query_update`, and `cast`. It also provides an `iterrows` method to iterate over the rows of the DataFrame.

    Attributes:
        content (dict): A dictionary representing the DataFrame, where each key is a column name and each value is a
            list of values for that column.

    Methods:
        __init__(self, content): Initializes a new FunctionalDF instance with the given content.
        __getitem__(self, key): Returns a FunctionalSeries or a dictionary of values for the given key.
        __len__(self): Returns the number of rows in the DataFrame.
        filter_content(self, key, expression): Returns a new FunctionalDF instance with the rows that match the given
            expression for the given key.
        query_update(self, key, expression, new_value): Returns a new FunctionalDF instance with the values that match
            the given expression for the given key replaced by the new value.
        cast(self, key, dtype, default): Returns a new FunctionalDF instance with the values for the given key cast to
            the given data type, or replaced by the default value if they cannot be cast.
        iterrows(self): Returns an iterable of ordered dictionaries, where each dictionary represents a row in the
            DataFrame.
        from_csv(date): Returns a new FunctionalDF instance with the content of the CSV file for the given date.
    """
    content = {}

    def __init__(self, content) -> None:
        if content:
            self.content = content

    def __getitem__(self, key: int | str) -> dict[str, str] | FunctionalSeries:
        if isinstance(key, str):
            return FunctionalSeries(self.content[key])
        return {k: v[key] for k, v in self.content.items()}
    
    def __len__(self) -> int:
        return len(list(self.content.values())[0])

    def filter_content(self, key: str, expression) -> "FunctionalDF":
        """
        Returns a new FunctionalDF object with only the rows that satisfy the given expression.

        Args:
            key (str): The key of the column to filter on.
            expression (function): A function that takes a single argument (the value of the column)
                and returns a boolean indicating whether the row should be included in the result.

        Returns:
            FunctionalDF: A new FunctionalDF object with only the rows that satisfy the given expression.
        """
        indexes = [i for i, x in enumerate(self.content[key]) if expression(x)]
        return FunctionalDF(
            {k: [v[i] for i in indexes] for k, v in self.content.items()}
        )

    def query_update(self, key: str, expression, new_value: Any) -> "FunctionalDF":
        """
        Update the values in a column of the dataframe based on a condition.

        Args:
            key (str): The name of the column to update.
            expression (function): A function that takes a value and returns a boolean indicating whether the value should be updated.
            new_value (Any): The new value to set for the matching rows.

        Returns:
            FunctionalDF: A new FunctionalDF object with the updated values.
        """
        indexes = [i for i, x in enumerate(self.content[key]) if expression(x)]
        return FunctionalDF(
            {
                k: [new_value if i in indexes else v for i, v in enumerate(value)]
                if key == k
                else value
                for k, value in self.content.items()
            }
        )
    
    def cast(self, key: str, dtype: type, default) -> "FunctionalDF":
        """
        Casts the values of a column to a specified data type, while replacing empty values with a default value.

        Args:
            key (str): The name of the column to cast.
            dtype (type): The data type to cast the column to.
            default: The default value to use for empty values.

        Returns:
            FunctionalDF: A new FunctionalDF object with the specified column casted to the specified data type.
        """

        return FunctionalDF(
            {
                k: [dtype(v) if v != "" else default for v in value]
                if k == key
                else value
                for k, value in self.content.items()
            }
        )
    
    def iterrows(self) -> Iterable[dict[str, str]]:
            """
            Iterate over DataFrame rows as ordered dictionaries.

            Returns:
                An iterable of ordered dictionaries, where each dictionary represents a row in the DataFrame.
            """
            return (dict(zip(self.content.keys(), t)) for t in zip(*self.content.values()))

    @staticmethod
    def from_csv(date: date) -> "FunctionalDF":
        """
        Create a FunctionalDF object from a CSV file.

        Args:
            date (date): The date of the CSV file to read.

        Returns:
            FunctionalDF: A FunctionalDF object containing the data from the CSV file.
        """

        with open(f"./data/{date.isoformat()}.csv", "r") as file:
            reader = csv.DictReader(file)
            content = dict(
                zip(
                    (i for i in reader.fieldnames),
                    zip(*map(lambda row: row.values(), reader)),
                )
            )
        return FunctionalDF(content)

