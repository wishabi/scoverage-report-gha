from dataclasses import dataclass
from typing import List


# ======================================
# Report processing
@dataclass
class CoverageEntry:
    name: str
    result: float
    is_package: bool
    threshold: float = None


@dataclass
class ReportCoverage:
    overall: CoverageEntry
    packages: List[CoverageEntry]


# ======================================
# PR comments
@dataclass
class CommentRow:
    name: str
    value: float
    icon: str


@dataclass
class Comment:
    msg: str
