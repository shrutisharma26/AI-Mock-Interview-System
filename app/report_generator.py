from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
        role,
        difficulty,
        score):

    filename = "interview_report.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(
        "AI Mock Interview Report",
        styles["Title"]
    )

    story.append(title)
    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Role: {role}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Difficulty: {difficulty}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Overall Score: {score}%",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    if score >= 70:
        feedback = (
            "Excellent performance. "
            "You are interview ready."
        )

    elif score >= 40:
        feedback = (
            "Good attempt. Practice more."
        )

    else:
        feedback = (
            "Needs significant improvement."
        )

    story.append(
        Paragraph(
            f"Feedback: {feedback}",
            styles["Normal"]
        )
    )

    doc.build(story)

    return filename