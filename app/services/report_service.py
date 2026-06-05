import uuid
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

REPORTS_DIR = Path("research_reports")
REPORTS_DIR.mkdir(exist_ok=True)

RECOMMENDATION_COLORS = {
    "buy": colors.HexColor("#27ae60"),
    "hold": colors.HexColor("#e67e22"),
    "sell": colors.HexColor("#e74c3c"),
}

IMPACT_COLORS = {
    "positive": colors.HexColor("#27ae60"),
    "negative": colors.HexColor("#e74c3c"),
    "neutral": colors.HexColor("#7f8c8d"),
}


def generate_research_report(brief: dict) -> str:
    report_id = str(uuid.uuid4())[:8].upper()
    company_slug = brief.get("company_name", "company").replace(" ", "_").replace(".", "")
    report_name = f"research_{report_id}_{company_slug}.pdf"
    report_path = REPORTS_DIR / report_name

    doc = SimpleDocTemplate(
        str(report_path),
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("title", parent=styles["Title"], fontSize=20, spaceAfter=4)
    heading = ParagraphStyle("heading", parent=styles["Heading2"], fontSize=12, spaceAfter=6)
    body = ParagraphStyle("body", parent=styles["Normal"], fontSize=10, leading=14, spaceAfter=4)
    small = ParagraphStyle("small", parent=styles["Normal"], fontSize=8, leading=12,
                           textColor=colors.HexColor("#666666"))

    story = []
    recommendation = (brief.get("recommendation") or "hold").lower()
    rec_color = RECOMMENDATION_COLORS.get(recommendation, colors.grey)

    # ── Header ───────────────────────────────────────────────
    company_name = brief.get("company_name", "Unknown Company")
    ticker = brief.get("ticker")
    title_text = f"{company_name} ({ticker})" if ticker else company_name

    story.append(Paragraph(title_text, title_style))
    story.append(Paragraph(
        f"Sector: {brief.get('sector') or 'N/A'}  |  "
        f"HQ: {brief.get('headquarters') or 'N/A'}  |  "
        f"Founded: {brief.get('founded') or 'N/A'}",
        small
    ))
    story.append(Paragraph(
        f"Report ID: {report_id}  |  Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}",
        small
    ))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2c3e50")))
    story.append(Spacer(1, 10))

    # ── Recommendation Banner ────────────────────────────────
    confidence_pct = f"{(brief.get('confidence') or 0) * 100:.0f}%"
    rec_table = Table(
        [[Paragraph(
            f"RECOMMENDATION: {recommendation.upper()}  |  CONFIDENCE: {confidence_pct}",
            ParagraphStyle(
                "rec", parent=styles["Normal"],
                fontSize=14, fontName="Helvetica-Bold",
                textColor=colors.white, alignment=1
            )
        )]],
        colWidths=[6.5 * inch],
    )
    rec_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), rec_color),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 16))

    # ── Business Overview ────────────────────────────────────
    story.append(Paragraph("Business Overview", heading))
    story.append(Paragraph(brief.get("business_overview") or "N/A", body))
    story.append(Spacer(1, 10))

    # ── Key Financials ───────────────────────────────────────
    story.append(Paragraph("Key Financials", heading))
    financials = brief.get("key_financials") or {}
    fin_data = [
        ["Metric", "Value"],
        ["Revenue", financials.get("revenue") or "N/A"],
        ["Net Income", financials.get("net_income") or "N/A"],
        ["Market Cap", financials.get("market_cap") or "N/A"],
        ["P/E Ratio", financials.get("pe_ratio") or "N/A"],
        ["Revenue Growth", financials.get("revenue_growth") or "N/A"],
    ]
    fin_table = Table(fin_data, colWidths=[3 * inch, 3.5 * inch])
    fin_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#dddddd")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(fin_table)
    story.append(Spacer(1, 14))

    # ── Strengths & Risks ────────────────────────────────────
    story.append(Paragraph("Strengths", heading))
    for s in (brief.get("strengths") or []):
        story.append(Paragraph(f"• {s}", body))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Risks", heading))
    for r in (brief.get("risks") or []):
        story.append(Paragraph(f"• {r}", body))
    story.append(Spacer(1, 10))

    # ── Recent News ──────────────────────────────────────────
    story.append(Paragraph("Recent News", heading))
    news_items = brief.get("recent_news") or []
    if news_items:
        news_data = [["Headline", "Impact"]]
        for item in news_items:
            news_data.append([
                item.get("headline", ""),
                item.get("impact", "neutral").upper(),
            ])
        news_table = Table(news_data, colWidths=[5.5 * inch, 1 * inch])
        news_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#dddddd")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            *[
                ("TEXTCOLOR", (1, i + 1), (1, i + 1),
                 IMPACT_COLORS.get(news_items[i].get("impact", "neutral"), colors.grey))
                for i in range(len(news_items))
            ],
            *[
                ("FONTNAME", (1, i + 1), (1, i + 1), "Helvetica-Bold")
                for i in range(len(news_items))
            ],
        ]))
        story.append(news_table)
    story.append(Spacer(1, 14))

    # ── Competitive Position ─────────────────────────────────
    story.append(Paragraph("Competitive Position", heading))
    story.append(Paragraph(brief.get("competitive_position") or "N/A", body))
    story.append(Spacer(1, 10))

    # ── Recommendation Rationale ─────────────────────────────
    story.append(Paragraph("Recommendation Rationale", heading))
    story.append(Paragraph(brief.get("recommendation_rationale") or "N/A", body))
    story.append(Spacer(1, 10))

    # ── Data Sources ─────────────────────────────────────────
    story.append(Paragraph("Data Sources", heading))
    sources = brief.get("data_sources") or []
    story.append(Paragraph(", ".join(sources) if sources else "N/A", small))
    story.append(Spacer(1, 10))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "This report was generated automatically by Financial Research Agent AI. "
        "It is for informational purposes only and does not constitute financial advice. "
        "Always conduct your own due diligence before making investment decisions.",
        small
    ))

    doc.build(story)
    return str(report_path)