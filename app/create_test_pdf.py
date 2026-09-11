from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


OUTPUT_FILE = Path(
    "knowledge/registration_requirements.pdf"
)


def create_test_pdf():

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    pdf = canvas.Canvas(
        str(OUTPUT_FILE),
        pagesize=A4
    )

    width, height = A4

    y = height - 60

    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawString(
        50,
        y,
        "REGISTRATION REQUIREMENTS"
    )

    y -= 40

    pdf.setFont(
        "Helvetica",
        11
    )

    requirements = [
        "1. Users must provide a unique username during registration.",
        "2. Usernames must contain between 5 and 20 characters.",
        "3. Users must provide a valid email address.",
        "4. Passwords must contain at least 8 characters.",
        "5. Passwords must contain at least one uppercase letter,",
        "   one lowercase letter, one number, and one special character.",
        "6. The email address must not already exist in the system.",
        "7. A verification email must be sent after successful registration."
    ]

    for line in requirements:

        pdf.drawString(
            50,
            y,
            line
        )

        y -= 25

    pdf.save()

    print(
        f"Created PDF: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    create_test_pdf()