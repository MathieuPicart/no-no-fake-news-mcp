from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    title = Column(String)
    score = Column(Integer)
    verdict_badge = Column(String)
    verdict_label = Column(String)
    verdict_color = Column(String)
    verdict_message = Column(String)
    details = Column(JSON)  # Stores linguistic, source, fact_check details
    created_at = Column(DateTime(timezone=True), server_default=func.now())
