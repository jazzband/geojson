from decimal import Decimal
from numbers import Real
from typing import (
    Callable,
    List,
    MutableMapping,
    Optional,
    Tuple,
    TypeAlias,
    TypeVar,
    Union,
)

from geojson.base import GeoJSON

# Python 3.7 doesn't support using isinstance() with Protocols
# Use checks for (Real, Decimal) instead
SupportsRound: TypeAlias = Union[Real, Decimal]

# Annotation for GeoJSON-like objects
# Multiple types used, because mutable collections are invariant
G = TypeVar('G', MutableMapping, dict, GeoJSON)

# Annotations for list-like containers (not GeoJSON instances)
PointLike: TypeAlias = Union[List[SupportsRound], Tuple[SupportsRound, ...]]
LineLike: TypeAlias = List[PointLike]
PolyLike: TypeAlias = List[LineLike]
MultiPolyLike: TypeAlias = List[PolyLike]
CoordsAny: TypeAlias = Union[
    PointLike, LineLike, PolyLike, MultiPolyLike, G, List[G]
]

# Annotations for GeoJSON validations
CheckValue = TypeVar('CheckValue', PointLike, LineLike)
ErrorSingle: TypeAlias = Optional[str]
ErrorList: TypeAlias = List[ErrorSingle]
CheckErrorFunc: TypeAlias = Callable[[CheckValue], ErrorSingle]
