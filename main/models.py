from dataclasses import dataclass
from typing import List
from enum import Enum


# ======================================
# Report processing
class CoverageType(Enum):
    OVERALL = 1
    PACKAGE = 2
    CHANGED_FILE = 3


@dataclass
class CoverageEntry:
    name: str
    result: float
    cov_type: CoverageType
    threshold: float = None


@dataclass
class ReportCoverage:
    overall: CoverageEntry
    packages: List[CoverageEntry]
    changed_files: List[CoverageEntry]


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
