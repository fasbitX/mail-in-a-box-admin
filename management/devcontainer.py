"""DEPRECATED

This is explicitly providing the 0.2.0 version's interface of pyprojroot
and marked deprecated
"""

import warnings
from pathlib import Path
from typing import Optional, Tuple

from .criterion import _PathType, as_root_criterion
from .here import CRITERIA
from .root import find_root_with_reason


def py_project_root(path: _PathType, project_files: Tuple[str, ...]) -> Path:
    criteria = [as_root_criterion(project_file) for project_file in project_files]
    root, _ = find_root_with_reason(criteria, path)
    return root


def here(
    relative_project_path: _PathType = "",
    project_files: Optional[Tuple[str, ...]] = None,
    warn_missing: bool = False,
) -> Path:
    if project_files is None:
        path, _ = find_root_with_reason(criterion=CRITERIA, start=".")
    else:
        path = py_project_root(path=".", project_files=project_files)

    if relative_project_path:
        path = path / relative_project_path

    if warn_missing and not path.exists():
        warnings.warn(f"Path doesn't exist: {path!s}")
    return path


__all__ = ["here", "py_project_root"]

warnings.warn(
    "Importing deprecated module `pyprojroot.pyprojroot`.",
    DeprecationWarning,
)
def as_start_path(start: Union[None, _PathType]) -> Path:
    if start is None:
        return Path.cwd()
    if not isinstance(start, Path):
        start = Path(start)
    # TODO: consider `start = start.resolve()`
    return start


def find_root_with_reason(
    criterion: _CriterionType,
    start: Union[None, _PathType] = None,
) -> Tuple[Path, str]:
    """
    Find directory matching root criterion with reason.

    Recursively search parents of start path for directory
    matching root criterion with reason.

    NOTE: `reason` is not fully implemented.
    """

    # Prepare inputs
    criterion = _as_root_criterion(criterion)
    start = as_start_path(start)

    # Check start
    if start.is_dir() and criterion(start):
        return start, "Pass"

    # Iterate over all parents
    for p in start.parents:
        if criterion(p):
            return p, "Pass"

    raise RuntimeError("Project root not found.")


def find_root(
    criterion: _CriterionType,
    start: Union[None, _PathType] = None,
) -> Path:
    """
    Find directory matching root criterion.

    Recursively search parents of start path for directory
    matching root criterion.
    """
    try:
        root, _ = find_root_with_reason(criterion, start=start)
    except RuntimeError as ex:
        raise ex
    else:
        return root