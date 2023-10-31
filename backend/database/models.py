from sqlalchemy import Column, DateTime, Index, Integer, Text
from sqlalchemy.dialects.postgresql import UUID as postgressUUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Impression(Base):
    __tablename__ = "impression"

    uuid = Column(postgressUUID(as_uuid=True), primary_key=True)
    impressions_count = Column(Integer, nullable=False)
    reg_time = Column(DateTime, nullable=False)
    mm_dma = Column(Integer, nullable=False)
    site_id = Column(Text, nullable=False)

    __table_args__ = (
        Index("idx_site_id", site_id, postgresql_using="btree"),
        Index("idx_mm_dma", mm_dma, postgresql_using="btree"),
    )


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    impression_uuid = Column(postgressUUID(as_uuid=True), nullable=False)
    tag = Column(Text, nullable=True)

    __table_args__ = (
        Index("idx_impression_uuid", impression_uuid, postgresql_using="hash"),
    )
