"""AOC INPUT UTILS
"""
import inspect
import sys
from pathlib import Path
from typing import Callable, Optional

import numpy as np


def read_input(
    input_path: Optional[str | Path] = None,
    as_type: Optional[Callable] = None,
    to_numpy: bool = False,
    np_dtype: Optional[np.dtype] = None,
    one_line: bool = False,
    separator: Optional[str] = ",",
) -> list:
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
        input_data = input_file.read().splitlines()

    if one_line:
        input_data = input_data[0] if not separator else input_data[0].split(separator)

    if as_type:
        input_data = list(map(as_type, input_data))

    if to_numpy:
        input_data = np.asarray(input_data, dtype=np_dtype)

    return input_data
