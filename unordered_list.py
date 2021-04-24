from typing import Hashable, Iterable, Generator
from values_counts import values_counts, values_counts_generator, ValueCountsIterator


class UnorderedList:
    """Behaves like a list but is unordered
       Like a set but can have multiples
       Values must be hashable i.e., no lists, sets, dicts

       Examples
       --------
       >>> UnorderedList([3, 2, 3, 1]) == UnorderedList([3, 3, 1, 2])
       True

       >>> UnorderedList([3, 2, 3, 1]) + [1, 1, 5]
       UnorderedList([1, 1, 1, 2, 3, 3, 5]

       >>> UnorderedList([3, 2, 3, 1]) - [1, 3]
       UnorderedList([2, 3])

       >>> UnorderedList([3, 2, 3, 1]) & [1, 1, 5]
       {1}

       >>> UnorderedList([3, 2, 3, 1]) | [1, 1, 5]
       {1, 2, 3, 5}

       >>> ul = UnorderedList([3, 2, 3, 1])
       >>> ul.append(1)
       >>> ul
       UnorderedList([1, 1, 2, 3, 3]

       >>> ul.extend([2, 5, 6, 6])
       >>> ul
       UnorderedList([1, 1, 2, 2, 3, 3, 5, 6, 6]

    """
    def __init__(self, vals) -> None:
        self._counts = values_counts(vals)

    def __repr__(self) -> str:
        values = self.__list__()
        return 'UnorderedList(' + str(values) + ')'

    def __iter__(self) -> ValueCountsIterator:
        return ValueCountsIterator(self._counts)

    def __len__(self) -> int:
        return sum(self._counts.values())

    def __eq__(self, other) -> bool:
        return self._counts == values_counts(other)

    def __add__(self, other):
        cpy = self.copy()
        cpy.extend(other)
        return cpy

    def __sub__(self, other):
        other_counts = values_counts(other)
        out = self.copy()
        for val, counts in other_counts.items():
            try:
                out._counts[val] -= counts
                if out._counts[val] <= 0:
                    del(out._counts[val])
            except KeyError:
                raise ValueError(f'{val} cannot be subtracted because it is not in UnorderedList.')
        return out

    def __contains__(self, val: Hashable) -> bool:
        return val in self._counts

    def __mul__(self, num: int):
        return {val:count*num for val, count in self._counts.items()}

    def __and__(self, other) -> set:
        return set(self._counts) & set(other)

    def __list__(self) -> list:
        return list(self.values_counts_generator())

    def __set__(self) -> set:
        return set(self._counts)

    def __or__(self, other) -> set:
        return self.__set__() | set(other)

    def append(self, val: Hashable) -> None:
        self._counts.setdefault(val, 0)
        self._counts[val] += 1

    def clear(self) -> None:
        self._counts.clear()

    def count(self, val: Hashable) -> int:
        if val in self._counts:
            return self._counts[val]
        return 0

    def copy(self):
        return UnorderedList(self.__list__())

    def extend(self, values: Iterable[Hashable]) -> None:
        for val, count in values_counts(values).items():
            self._counts.setdefault(val, 0)
            self._counts[val] += count

    def insert(self, val: Hashable) -> None:
        self.append(val)

    def pop(self, val=None) -> Hashable:
        if len(self) == 0:
            raise ValueError('pop from empty list')
        if val is None:
            val = list(self._counts.keys())[-1]
        self.remove(val)
        return val

    def remove(self, val: Hashable) -> None:
        self._counts[val] -= 1
        if self._counts[val] <= 0:
            del(self._counts[val])

    def values_counts(self) -> dict[Hashable, int]:
        return self._counts

    def values_counts_generator(self) -> Generator[Hashable, None, None]:
        return values_counts_generator(self._counts)

