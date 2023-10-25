from enum import StrEnum


class EventType(StrEnum):
    fclick = "fclick"
    registration = "registration"
    content = "content"
    lead = "lead"
    signup = "signup"
    misc = "misc"


class AggregationField(StrEnum):
    site = "site_id"
    dma = "mm_dma"
