from typing import Hashable, Generator, Iterable


def values_counts(values: Iterable[Hashable]) -> dict[Hashable, int]:
    """Takes a iterable of values
       return a dictionary of the counts of each value
       vc = value_counts(['a', 'a', 'b', 'c', 'c', 'c'])
       vc -> {'a':2, 'b':1, 'c':3}
    """
    values = list(values)
    return {val:values.count(val) for val in set(values)}


def values_counts_generator(counts: dict[Hashable, int]) -> Generator[Hashable, None, None]:
    """Returns a generator that yields values from a value_counts dictionary
       vc = {'a':2, 'b':1, 'c':3}
       gen = value_counts_generator(vc)
       list(gen) -> ['a', 'a', 'b', 'c', 'c', 'c']
    """
    for key in counts.keys():
        i = 1
        count = counts[key]
        while i <= count:
            yield key
            i += 1


class ValueCountsIterator:
        def __init__(self, counts: dict[Hashable, int]):
            self.vc = values_counts_generator(counts)
        
        def __next__(self) -> Hashable:
            for val in self.vc:
                return val
            raise StopIteration