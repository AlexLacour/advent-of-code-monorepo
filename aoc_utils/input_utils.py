"""AOC INPUT UTILS"""

import inspect
from pathlib import Path
from typing import Any, Callable, Literal, Optional, TypeVar, overload

import numpy as np

# # type overloads
T = TypeVar("T")


@overload
def read_input(
    *,
    raw_input: Literal[True],
) -> str: ...


@overload
def read_input(
    *,
    as_type: ...,
    to_numpy: Literal[True],
) -> np.ndarray: ...


@overload
def read_input(
    *,
    as_type: Callable[..., T],
    to_numpy: Literal[False] = ...,
) -> list[T]: ...


@overload
def read_input(
    *, as_type: Callable[..., T], one_line: Literal[True], separator: ...
) -> T: ...


@overload
def read_input() -> list[str]: ...


@overload
def read_input(*, one_line: Literal[True], separator: None) -> str: ...


# Function Logic
def read_input(
    input_path: Optional[str | Path] = None,
    as_type: Optional[Callable] = None,
    to_numpy: bool = False,
    np_dtype: Optional[np.dtype] = None,
    one_line: bool = False,
    separator: Optional[str] = ",",
    raw_input: bool = False,
) -> Any:
    if input_path is None:
        calling_file_path = Path(inspect.stack()[-1].filename)
        calling_file_name = calling_file_path.stem

        if not calling_file_name.isnumeric():
            raise ValueError(
                "If input path is not specified, the calling file should be named X.py, "
                "with X being the number of the AdventOfCode day challenge."
            )

        calling_file_year = calling_file_path.parent.parent

        input_path = calling_file_year / f"inputs/{calling_file_name}.txt"

    with open(input_path) as input_file:
        if raw_input:
            input_data = input_file.read()
        else:
            input_data = input_file.read().splitlines()

    if as_type:
        input_data = list(map(as_type, input_data))

    if one_line:
        input_data = (
            input_data[0] if not separator else input_data[0].split(separator)
        )

    if to_numpy:
        input_data = np.asarray(input_data, dtype=np_dtype)

    return input_data
