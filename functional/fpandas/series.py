from typing import Any, Iterable

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
