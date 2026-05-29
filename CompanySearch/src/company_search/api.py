import asyncio
import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from company_search.crew import CompanySearch

app = FastAPI(title="CompanySearch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent.parent.parent
RESULTS_DIR = BASE_DIR / "results"
FRONTEND_DIR = BASE_DIR / "frontend"
RESULTS_DIR.mkdir(exist_ok=True)

jobs: Dict[str, dict] = {}


class SearchRequest(BaseModel):
    company_name: str


def _slugify(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "_", slug)
    return slug.strip("_")


def _result_folder(company_name: str) -> Path:
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = _slugify(company_name)
    base = f"{slug}_{date_str}"
    folder = RESULTS_DIR / base
    if folder.exists():
        time_str = datetime.now().strftime("%H%M")
        folder = RESULTS_DIR / f"{base}_{time_str}"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _run_crew(company_name: str, job_id: str) -> None:
    try:
        result = CompanySearch().crew().kickoff(inputs={"company_name": company_name})

        if result.pydantic:
            report = result.pydantic.model_dump()
        elif result.json_dict:
            report = result.json_dict
        else:
            # Best-effort parse from raw
            raw = result.raw.strip()
            # Strip possible markdown fences
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
            try:
                report = json.loads(raw)
            except json.JSONDecodeError:
                report = {"company_name": company_name, "about": raw, "news": []}

        if "company_name" not in report:
            report["company_name"] = company_name

        folder = _result_folder(company_name)
        payload = {
            **report,
            "searched_at": datetime.now().isoformat(),
            "folder": folder.name,
        }
        (folder / "result.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        jobs[job_id] = {"status": "done", "result": payload, "folder": folder.name}
    except Exception as exc:
        jobs[job_id] = {"status": "error", "error": str(exc)}


@app.post("/api/search")
async def search(request: SearchRequest):
    if not request.company_name.strip():
        raise HTTPException(400, "Company name is required")
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "running"}
    asyncio.create_task(asyncio.to_thread(_run_crew, request.company_name, job_id))
    return {"job_id": job_id}


@app.get("/api/search/{job_id}")
async def get_job(job_id: str):
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    return jobs[job_id]


@app.get("/api/history")
async def history():
    items = []
    if not RESULTS_DIR.exists():
        return items
    for folder in sorted(RESULTS_DIR.iterdir(), key=lambda p: p.name, reverse=True):
        result_file = folder / "result.json"
        if not result_file.exists():
            continue
        data = json.loads(result_file.read_text(encoding="utf-8"))
        items.append(
            {
                "folder": folder.name,
                "company_name": data.get("company_name", folder.name),
                "searched_at": data.get("searched_at", ""),
                "news_count": len(data.get("news", [])),
            }
        )
    return items


@app.get("/api/history/{folder}")
async def history_item(folder: str):
    result_file = RESULTS_DIR / folder / "result.json"
    if not result_file.exists():
        raise HTTPException(404, "Result not found")
    return json.loads(result_file.read_text(encoding="utf-8"))


@app.get("/api/history/{folder}/pdf")
async def history_pdf(folder: str):
    result_file = RESULTS_DIR / folder / "result.json"
    if not result_file.exists():
        raise HTTPException(404, "Result not found")
    data = json.loads(result_file.read_text(encoding="utf-8"))
    pdf_path = RESULTS_DIR / folder / "report.pdf"
    _generate_pdf(data, pdf_path)
    return FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename=f"{folder}.pdf",
    )


def _generate_pdf(data: dict, output_path: Path) -> None:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        spaceAfter=4,
        textColor=colors.HexColor("#1e40af"),
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=12,
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=14,
        spaceAfter=6,
        textColor=colors.HexColor("#1e40af"),
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        spaceAfter=10,
    )
    date_style = ParagraphStyle(
        "NewsDate",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#64748b"),
        spaceBefore=8,
    )
    headline_style = ParagraphStyle(
        "NewsHeadline",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        spaceAfter=2,
    )
    source_style = ParagraphStyle(
        "NewsSource",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#94a3b8"),
        spaceAfter=4,
    )

    story.append(Paragraph(data.get("company_name", ""), title_style))
    searched_at = data.get("searched_at", "")[:10]
    story.append(Paragraph(f"Research report · {searched_at}", subtitle_style))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#e2e8f0")))

    story.append(Paragraph("About", section_style))
    story.append(Paragraph(data.get("about", ""), body_style))

    story.append(Paragraph("Latest News", section_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0")))

    for item in data.get("news", []):
        story.append(Spacer(1, 0.2 * cm))
        story.append(Paragraph(item.get("date", ""), date_style))
        story.append(Paragraph(item.get("headline", ""), headline_style))
        story.append(Paragraph(item.get("description", ""), body_style))
        if item.get("source"):
            story.append(Paragraph(f"Source: {item['source']}", source_style))
        story.append(HRFlowable(width="100%", thickness=0.3, color=colors.HexColor("#f1f5f9")))

    doc.build(story)


# Serve the frontend — must be last to avoid shadowing API routes
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


def main():
    import uvicorn
    uvicorn.run("company_search.api:app", host="0.0.0.0", port=8000, reload=False)
