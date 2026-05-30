from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class ResearchReport(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    report_id: str
    company_name: str
    ticker: Optional[str] = None
    sector: Optional[str] = None
    recommendation: Optional[str] = None   # Buy / Hold / Sell
    confidence: Optional[float] = None
    summary: Optional[str] = None
    report_pdf_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)