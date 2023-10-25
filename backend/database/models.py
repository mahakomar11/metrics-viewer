from sqlalchemy import Column, DateTime, Integer, Text
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


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    impression_uuid = Column(postgressUUID(as_uuid=True), nullable=False)
    tag = Column(Text, nullable=True)
