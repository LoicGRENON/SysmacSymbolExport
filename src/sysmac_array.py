import copy
import re
from dataclasses import dataclass
from itertools import product
from typing import List


from sysmac_data_type import SysmacDataType, BASE_TYPES, INTERNAL_TYPES


@dataclass
class ArrayDimension:
    lower: int
    upper: int

    @property
    def size(self) -> int:
        return self.upper - self.lower + 1


class SysmacArray:
    def __init__(self, symbol: SysmacDataType):
        self.symbol = symbol
        self._dimensions: List[ArrayDimension] = []
        self._base_type: str = ""
        self.parse()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.symbol.base_type})'

    def parse(self):
        match = re.match(r"ARRAY\[(.+)\] OF (\S+)", self.symbol.base_type, re.IGNORECASE)
        if not match:
            raise ValueError(f"Incorrect format.\n"
                             f"Expected: ARRAY[a..b(, c..d)] OF TYPE\n"
                             f"Got: {self.symbol.base_type}")

        ranges_part, data_type = match.groups()
        self._base_type = data_type

        self._dimensions = []
        for dim in ranges_part.split(','):
            dim = dim.strip()
            bounds_match = re.match(r"(-?\d+)\.\.(-?\d+)", dim)
            if not bounds_match:
                raise ValueError(f"Invalid range: {dim}")
            lower, upper = map(int, bounds_match.groups())
            self._dimensions.append(ArrayDimension(lower, upper))

    @property
    def base_type(self) -> str:
        return self._base_type

    @property
    def is_base_type(self):
        return self.base_type in BASE_TYPES

    @property
    def is_internal_type(self):
        return self.base_type in INTERNAL_TYPES.keys()

    @property
    def dimensions(self) -> List[ArrayDimension]:
        return self._dimensions

    def expand(self) -> List[SysmacDataType]:
        dim = [range(d.lower, d.upper + 1) for d in self._dimensions]
        dim_values = product(*dim)

        # Array of base type -> Do not expand more
        #  eg: It should return "aCptNDef" from type "USINT[0..19,1..2]"
        #  instead of "aCptNDef[0,1]", "aCptNDef[0,2], ..." from type "USINT"
        if self._base_type in BASE_TYPES:
            ranges = ','.join([f'{self._dimensions[i].lower}..{self._dimensions[i].upper}'
                               for i, d in enumerate(self._dimensions)])
            self.symbol.base_type = f'{self._base_type}[{ranges}]'
            return [self.symbol]

        # Array of user type -> Each index of the array is a symbol for further expanding
        res = []
        for d in dim_values:
            new_symbol = copy.deepcopy(self.symbol)
            new_symbol.name = f'{self.symbol.name}[{','.join(map(str, d))}]'
            new_symbol.base_type = self._base_type
            res.append(new_symbol)
        return res
