"""
report_generator.py
Builds a downloadable PDF analysis report using ReportLab.
"""
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
)


def build_analysis_pdf(output_path: str, user_name: str, resume_filename: str, analysis):
    """
    analysis: an Analysis SQLAlchemy object (JSON fields already decoded by caller)
    or a plain dict with the same keys.
    """
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleCustom", parent=styles["Title"], textColor=colors.HexColor("#4F46E5")
    )
    heading_style = ParagraphStyle(
        "HeadingCustom", parent=styles["Heading2"], textColor=colors.HexColor("#1E293B"),
        spaceBefore=12, spaceAfter=6,
    )
    body_style = styles["BodyText"]

    story = []
    story.append(Paragraph("AI Resume Analyzer &amp; Career Coach", title_style))
    story.append(Paragraph("Resume Analysis Report", styles["Heading3"]))
    story.append(Spacer(1, 12))

    meta = [
        ["Candidate", user_name],
        ["Resume File", resume_filename],
        ["Predicted Role", analysis["predicted_role"]],
        ["Overall Score", f"{analysis['overall_score']} / 100"],
        ["ATS Score", f"{analysis['ats_score']} / 100"],
    ]
    t = Table(meta, colWidths=[5 * cm, 10 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EEF2FF")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 16))

    story.append(Paragraph("Matched Skills", heading_style))
    matched = analysis.get("matched_skills") or []
    story.append(Paragraph(", ".join(s.title() for s in matched) or "None detected", body_style))

    story.append(Paragraph("Missing Skills (for target role)", heading_style))
    missing = analysis.get("missing_skills") or []
    story.append(Paragraph(", ".join(s.title() for s in missing) or "None — great coverage!", body_style))

    story.append(Paragraph("ATS Compatibility Issues", heading_style))
    ats_issues = analysis.get("ats_issues") or []
    if ats_issues:
        story.append(ListFlowable(
            [ListItem(Paragraph(i, body_style)) for i in ats_issues],
            bulletType="bullet",
        ))

    story.append(Paragraph("Learning Recommendations", heading_style))
    recs = analysis.get("learning_recommendations") or []
    if recs:
        rows = [["Skill", "Recommended Resource"]] + [[r["skill"], r["resource"]] for r in recs]
        rt = Table(rows, colWidths=[4 * cm, 11 * cm])
        rt.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(rt)

    story.append(Paragraph("AI-Generated Improvement Suggestions", heading_style))
    story.append(Paragraph((analysis.get("ai_suggestions") or "").replace("\n", "<br/>"), body_style))

    story.append(Paragraph("Sample Interview Questions", heading_style))
    questions = analysis.get("interview_questions") or []
    if questions:
        story.append(ListFlowable(
            [ListItem(Paragraph(q, body_style)) for q in questions],
            bulletType="1",
        ))

    doc.build(story)
    return output_path
