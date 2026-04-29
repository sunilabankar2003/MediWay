from pathlib import Path
import textwrap

SRC = Path("FA1_Activity_Details_MediWay.md")
OUT = Path("FA1_Activity_Details_MediWay.pdf")


def read_lines():
    text = SRC.read_text(encoding="utf-8")
    raw = [line.rstrip() for line in text.splitlines()]
    lines = []
    for line in raw:
        if line.startswith("#"):
            line = line.lstrip("#").strip().upper()
        if line.startswith("|") and line.endswith("|"):
            # keep tables readable in plain PDF flow
            parts = [p.strip() for p in line.strip("|").split("|")]
            line = " | ".join(parts)
        lines.append(line)
    return lines


def build_with_reportlab(lines):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(str(OUT), pagesize=A4)
    width, height = A4
    x = 50
    y = height - 50
    max_chars = 105

    for line in lines:
        wrapped = textwrap.wrap(line, width=max_chars) if line else [""]
        for w in wrapped:
            if y < 50:
                c.showPage()
                y = height - 50
            c.drawString(x, y, w)
            y -= 14
    c.save()


def build_with_fpdf(lines):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    for line in lines:
        line = line.encode("latin-1", errors="replace").decode("latin-1")
        pdf.multi_cell(0, 7, txt=line if line else " ")
    pdf.output(str(OUT))


def main():
    lines = read_lines()
    try:
        build_with_reportlab(lines)
        print(f"Created PDF with reportlab: {OUT.resolve()}")
        return
    except Exception as e:
        print(f"reportlab unavailable/failed: {e}")

    try:
        build_with_fpdf(lines)
        print(f"Created PDF with fpdf: {OUT.resolve()}")
        return
    except Exception as e:
        raise RuntimeError(f"Could not create PDF. reportlab/fpdf both failed. Last error: {e}")


if __name__ == "__main__":
    main()

