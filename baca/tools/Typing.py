import abjad
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

Number = Union[int, float]

OptionalBool = Union[bool, None]

OptionalInt = Union[int, None]

OptionalOrderedDict = Union[abjad.OrderedDict, None]

OptionalNumber = Union[Number, None]

OptionalStr = Union[str, None]

NumberPair = Tuple[Number, Number]
