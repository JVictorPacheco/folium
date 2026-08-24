from enum import StrEnum


class PageMode(StrEnum):
    FIXED = "fixed"
    CONTINUOUS = "continuous"


class AssetKind(StrEnum):
    IMAGE = "image"
    PDF = "pdf"
