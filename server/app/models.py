import uuid
from sqlalchemy import Column, String, Numeric, Date, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class IPO(Base):
    __tablename__ = "ipo_details"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_name = Column(String, nullable=False)
    industry = Column(String, nullable=True)
    issue_size = Column(Numeric, nullable=True)
    price_band = Column(String, nullable=True)
    issue_type = Column(String, nullable=True)
    ipo_type = Column(String, nullable=True)
    fresh_issue = Column(String, nullable=True)
    offer_for_sale = Column(String, nullable=True)
    listing_date = Column(Date, nullable=True)
    ipo_open_date = Column(Date, nullable=True)
    ipo_close_date = Column(Date, nullable=True)
    rhp_file_path = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
