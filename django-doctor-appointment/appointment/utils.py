def _pdf_escape(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _sanitize(text):
    if text is None:
        return ""
    try:
        return str(text)
    except Exception:
        return ""


def generate_confirmation_pdf(booking):
    # Minimal PDF generator with a few text lines (ASCII-safe).
    lines = [
        "Appointment Confirmation",
        "",
        f"Booking ID: {_sanitize(booking.booking_id)}",
        f"Patient Name: {_sanitize(booking.full_name)}",
        f"Phone: {_sanitize(booking.phone_number)}",
        f"Doctor: {_sanitize(booking.appointment.full_name)}",
        f"Department: {_sanitize(booking.appointment.department)}",
        f"Date: {_sanitize(booking.date)}",
        "",
        "Please bring this confirmation on your visit.",
    ]

    safe_lines = []
    for line in lines:
        safe_lines.append(_pdf_escape(line.encode("ascii", "ignore").decode("ascii")))

    # Simple text content stream
    y = 770
    leading = 16
    content_lines = ["BT", "/F1 12 Tf", f"72 {y} Td"]
    for idx, line in enumerate(safe_lines):
        if idx > 0:
            content_lines.append(f"0 -{leading} Td")
        content_lines.append(f"({line}) Tj")
    content_lines.append("ET")
    content = "\n".join(content_lines).encode("ascii")

    objects = []

    def add_obj(body):
        objects.append(body)

    add_obj("<< /Type /Catalog /Pages 2 0 R >>")
    add_obj("<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    add_obj("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>")
    add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    add_obj(f"<< /Length {len(content)} >>\nstream\n{content.decode('ascii')}\nendstream")

    xref_positions = []
    pdf = ["%PDF-1.4"]
    for i, obj in enumerate(objects, start=1):
        xref_positions.append(sum(len(s.encode("ascii")) + 1 for s in pdf))
        pdf.append(f"{i} 0 obj\n{obj}\nendobj")

    xref_start = sum(len(s.encode("ascii")) + 1 for s in pdf)
    xref = ["xref", f"0 {len(objects) + 1}", "0000000000 65535 f "]
    for pos in xref_positions:
        xref.append(f"{pos:010d} 00000 n ")
    trailer = [
        "trailer",
        f"<< /Size {len(objects) + 1} /Root 1 0 R >>",
        "startxref",
        str(xref_start),
        "%%EOF",
    ]

    pdf_bytes = ("\n".join(pdf) + "\n" + "\n".join(xref) + "\n" + "\n".join(trailer)).encode("ascii")
    return pdf_bytes
