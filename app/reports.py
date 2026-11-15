
import json
from datetime import datetime
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


def create_investigation_pdf(case, record, guide):
    """
    Generate a PDF investigation report from a saved record.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#403080"),
        alignment=TA_CENTER,
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#403080"),
        spaceBefore=15,
        spaceAfter=8
    )

    normal_style = styles["BodyText"]

    story = []

    def add_section(title, content):
        story.append(Paragraph(title, heading_style))

        safe_content = escape(str(content or "Not provided"))
        safe_content = safe_content.replace("\n", "<br/>")

        story.append(
            Paragraph(safe_content, normal_style)
        )

        story.append(Spacer(1, 8))

    # Report title
    story.append(
        Paragraph("FORENQUEST", title_style)
    )

    story.append(
        Paragraph(
            "Digital Forensics Investigation Report",
            ParagraphStyle(
                "Subtitle",
                parent=normal_style,
                alignment=TA_CENTER,
                fontSize=12
            )
        )
    )

    story.append(Spacer(1, 20))

    # Report information
    report_date = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    information = [
        ["Report Date", report_date],
        ["Investigator", record["investigator_name"] or "Not provided"],
        ["Case Title", case["title"]],
        ["Difficulty", case["level"]],
        ["Case ID", case["id"]]
    ]

    information_table = Table(
        information,
        colWidths=[1.6 * inch, 4.8 * inch]
    )

    information_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1),
             colors.HexColor("#EAE5F7")),
            ("TEXTCOLOR", (0, 0), (-1, -1),
             colors.HexColor("#222222")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ])
    )

    story.append(information_table)

    # Investigation findings
    add_section(
        "1. Investigation Findings",
        record["findings"]
    )

    # Evidence documentation
    add_section(
        "2. Evidence Documentation",
        record["evidence_notes"]
    )

    # Investigation questions and answers
    story.append(
        Paragraph("3. Investigation Questions & Answers",
                  heading_style)
    )

    saved_answers = json.loads(
        record["answers"] or "{}"
    )

    for index, question in enumerate(guide["questions"]):

        answer = saved_answers.get(
            str(index),
            "Not answered"
        )

        story.append(
            Paragraph(
                f"<b>Question {index + 1}:</b> "
                f"{escape(str(question))}",
                normal_style
            )
        )

        safe_answer = escape(str(answer or "Not answered"))
        safe_answer = safe_answer.replace("\n", "<br/>")

        story.append(
            Paragraph(
                f"<b>Answer:</b> {safe_answer}",
                normal_style
            )
        )

        story.append(Spacer(1, 10))

    # Report disclaimer
    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "End of Report",
            ParagraphStyle(
                "EndReport",
                parent=normal_style,
                alignment=TA_CENTER,
                textColor=colors.grey
            )
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer
