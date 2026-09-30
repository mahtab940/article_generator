from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.units import cm


def generate_pdf(report, filename="output/article.pdf"):
    document = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    content = []

    # Title
    content.append(
        Paragraph(report.title, title_style)
    )
    content.append(Spacer(1, 20))

    # Abstract
    content.append(
        Paragraph("Abstract", heading_style)
    )
    content.append(
        Paragraph(report.abstract, body_style)
    )
    content.append(Spacer(1, 15))

    # Introduction
    content.append(
        Paragraph("Introduction", heading_style)
    )
    content.append(
        Paragraph(report.introduction, body_style)
    )
    content.append(Spacer(1, 15))

    # Main sections
    for section in report.sections:
        content.append(
            Paragraph(section.heading, heading_style)
        )

        content.append(
            Paragraph(section.content, body_style)
        )

        content.append(Spacer(1, 15))

    # Conclusion
    content.append(
        Paragraph("Conclusion", heading_style)
    )
    content.append(
        Paragraph(report.conclusion, body_style)
    )
    content.append(Spacer(1, 15))

    # References
    content.append(
        Paragraph("References", heading_style)
    )

    for reference in report.references:
        reference_text = (
            f"{reference.authors} "
            f"({reference.year}). "
            f"<i>{reference.title}</i>. "
            f"{reference.url}"
        )

        content.append(
            Paragraph(reference_text, body_style)
        )

        content.append(Spacer(1, 8))

    document.build(content)

    print(f"PDF created: {filename}")
