from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


BASE_DIR = Path(__file__).resolve().parent.parent
INVOICE_DIR = BASE_DIR / "media" / "invoices"

INVOICE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def generate_invoice(
    username: str,
    plan_name: str,
    price: float,
    start_date: datetime,
    end_date: datetime,
    transaction_id: str
) -> str:

    filename = f"{transaction_id}.pdf"
    file_path = INVOICE_DIR / filename

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=A4
    )

    width, height = A4

    # Title
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(
        50,
        height - 60,
        "Blog Management API"
    )

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(
        50,
        height - 100,
        "Subscription Invoice"
    )

    # Invoice details
    pdf.setFont("Helvetica", 11)

    y = height - 150

    details = [
        f"User Name: {username}",
        f"Plan: {plan_name}",
        f"Price: Rs. {price:.2f}",
        f"Start Date: {start_date.strftime('%Y-%m-%d %H:%M:%S')}",
        f"End Date: {end_date.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Transaction ID: {transaction_id}",
    ]

    for detail in details:
        pdf.drawString(50, y, detail)
        y -= 30

    # Footer
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(
        50,
        60,
        "This is a generated invoice for subscription billing."
    )

    pdf.save()

    return f"/media/invoices/{filename}"
