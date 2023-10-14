from typing import Any, Iterable
from functools import reduce

_sum = lambda arr: reduce(lambda x, y: x + y, arr)
_len = lambda arr: reduce(lambda x, y: x + 1, arr, 0)
_min = lambda arr: reduce(lambda x, y: x if x < y else y, arr)
_max = lambda arr: reduce(lambda x, y: y if x < y else x, arr)

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
    
    def tolist(self):
        return self.serie
    
    def toset(self):
        return set(self.serie)

    def mean(self):
        self._to_int()
        return _sum(self.serie) / _len(self.serie)
    
    def median(self):
        self._to_int()
        length = _len(self.serie)
        sorted_serie = sorted(self.serie)
    
        if length % 2 == 0:
            return (sorted_serie[length // 2] + sorted_serie[length // 2 + 1]) / 2
    
        return sorted_serie[length // 2]
    
    def min(self):
        self._to_int()
        return _min(self.serie)
    
    def max(self):
        self._to_int()
        return _max(self.serie)
