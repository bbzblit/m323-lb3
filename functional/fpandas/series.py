from typing import Any, Iterable
from functools import reduce

_sum = lambda arr: reduce(lambda x, y: x + y, arr)
_len = lambda arr: reduce(lambda x, y: x + 1, arr, 0)
_min = lambda arr: reduce(lambda x, y: x if x < y else y, arr)
_max = lambda arr: reduce(lambda x, y: y if x < y else x, arr)

class FunctionalSeries:
    """
    A class representing a functional series.

    Attributes:
    dtype (type): The data type of the series.
    serie (list): The list of elements in the series.
    """

    dtype = str
    serie = []

    def __init__(self, it: Iterable) -> None:
        """
        Initializes a FunctionalSeries object.

        Args:
        it (Iterable): An iterable object containing the elements of the series.
        """
        self.serie = list(it)

    def _to_int(self):
        """
        Converts the elements of the series to float data type.
        """
        if self.dtype != float:
            self.serie = list(map(float, self))
            self.dtype = float
        
    def __getitem__(self, __name: int) -> Any:
        """
        Returns the element at the specified index.

        Args:
        __name (int): The index of the element to be returned.

        Returns:
        Any: The element at the specified index.
        """
        return self.serie[__name]
    
    def __str__(self) -> str:
        """
        Returns a string representation of the series.

        Returns:
        str: A string representation of the series.
        """
        return str(self.serie)
    
    def tolist(self):
        """
        Returns the series as a list.

        Returns:
        list: The series as a list.
        """
        return self.serie
    
    def toset(self):
        """
        Returns the series as a set.

        Returns:
        set: The series as a set.
        """
        return set(self.serie)

    def mean(self):
        """
        Returns the mean of the series.

        Returns:
        float: The mean of the series.
        """
        self._to_int()
        return _sum(self.serie) / _len(self.serie)
    
    def median(self):
        """
        Returns the median of the series.

        Returns:
        float: The median of the series.
        """
        self._to_int()
        length = _len(self.serie)
        sorted_serie = sorted(self.serie)
        return sorted_serie[length // 2]
    
    def min(self):
        """
        Returns the minimum value in the series.

        Returns:
        float: The minimum value in the series.
        """
        self._to_int()
        return _min(self.serie)
    
    def max(self):
        """
        Returns the maximum value in the series.

        Returns:
        float: The maximum value in the series.
        """
        self._to_int()
        return _max(self.serie)
