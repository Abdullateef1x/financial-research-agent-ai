from app.agent.researcher import run_research_agent
from app.db.database import get_session
from app.models.research import ResearchReport
from app.services.report_service import generate_research_report
from app.services.storage_service import upload_report_to_r2
from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
from pydantic import BaseModel
from sqlmodel import Session, select, desc

router = APIRouter(tags=["Research"])


class ResearchRequestModel(BaseModel):
    company_name: str


@router.post("/research")
def research_company(
    request: ResearchRequestModel,
    session: Session = Depends(get_session)
):
    try:
        brief = run_research_agent(request.company_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research agent failed: {e}")

    try:
        report_path = generate_research_report(brief)
        report_url = upload_report_to_r2(report_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {e}")

    report_id = Path(report_path).stem.split("_")[1]
    record = ResearchReport(
        report_id=report_id,
        company_name=brief.get("company_name") or request.company_name,
        ticker=brief.get("ticker"),
        sector=brief.get("sector"),
        recommendation=brief.get("recommendation"),
        confidence=brief.get("confidence") or 0.0,
        summary=brief.get("business_overview"),
        report_pdf_url=report_url,
    )
    session.add(record)
    session.commit()
    session.refresh(record)

    return {
        "report_id": report_id,
        "company": brief.get("company_name"),
        "ticker": brief.get("ticker"),
        "sector": brief.get("sector"),
        "recommendation": brief.get("recommendation"),
        "confidence": brief.get("confidence"),
        "summary": brief.get("business_overview"),
        "report_url": report_url,
        "created_at": record.created_at,
    }


@router.get("/reports")
def list_reports(session: Session = Depends(get_session)):
    reports = session.exec(
        select(ResearchReport).order_by(desc(ResearchReport.created_at))
    ).all()
    return {
        "total": len(reports),
        "reports": [
            {
                "report_id": r.report_id,
                "company": r.company_name,
                "ticker": r.ticker,
                "sector": r.sector,
                "recommendation": r.recommendation,
                "confidence": r.confidence,
                "created_at": r.created_at,
                "report_url": r.report_pdf_url,
            }
            for r in reports
        ]
    }