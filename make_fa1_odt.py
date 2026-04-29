import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

BASE_ODT = Path("fa_plan.odt")
OUT_ODT = Path("FA1_Activity_Details_MediWay.odt")

NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)

content_lines = [
    "FA-1 Activity Details (FYMCA Sem-II)",
    "Subject: Software Project Management",
    "Project: MediWay (Django-Based Online Pharmacy Management System)",
    "",
    "Student Name: ____________________",
    "PRN/Roll No.: ____________________",
    "Division: ____________________",
    "Date: ____________________",
    "",
    "1) Life Cycle Model Selection and Justification (4 Marks)",
    "Selected Model: Hybrid (Agile + Waterfall)",
    "For MediWay, we used a Hybrid model because core architecture was planned first, then features were iteratively improved.",
    "- Waterfall-like stages: requirement analysis, DB schema design, initial routing and authentication setup.",
    "- Agile iterations: prescription upload flow, Razorpay integration, fuzzy search, pagination, admin order tracking.",
    "Justification: this model gave predictability for core design and flexibility for changing functional needs.",
    "",
    "2) Team Structure and Sudden Member Exit Scenario (4 Marks)",
    "Team roles:",
    "1. Project Lead / Full-Stack Integrator",
    "2. Backend Developer (Django models, business logic, payment flow)",
    "3. Frontend Developer (templates, UI flow, responsiveness)",
    "4. QA and Documentation Member (test cases, defect logs, final report)",
    "Scenario: Backend Developer leaves 2 weeks before submission.",
    "Impact: payment and order flows become high-risk; integration and bug-fix speed drops.",
    "Mitigation: shared repo discipline, module documentation, cross-skilling, feature freeze, role reallocation and regression testing.",
    "",
    "3) Risk Management: Top 3 Risks with Prioritization (4 Marks)",
    "Risk 1 (Priority 1 - Technical): Payment verification mismatch/failure in Razorpay callback or status sync.",
    "Risk 2 (Priority 2 - Schedule): Delay in integrating prescription, checkout, and order-status modules.",
    "Risk 3 (Priority 3 - Resource): Team member unavailability during final integration and testing.",
    "Mitigation summary:",
    "- Technical: sandbox testing, error handling, transaction logging, status reconciliation checks.",
    "- Schedule: milestone-based plan, weekly review, early integration tests.",
    "- Resource: backup ownership, handover notes, pair programming on critical modules.",
    "",
    "4) Leadership Style Application (4 Marks)",
    "Directive style situation:",
    "Before demo, checkout fails for prescription-required medicines.",
    "Lead immediately freezes non-critical tasks, assigns focused owners, and runs strict checkpoint reviews.",
    "Collaborative style situation:",
    "During feature improvement planning (search relevance and admin dashboard usability).",
    "Lead gathers ideas from all members, prioritizes by effort-impact, and finalizes tasks jointly.",
    "",
    "5) Gantt Chart / Project Schedule (4 Marks)",
    "Major Activities with 8-week timeline:",
    "W1-W2: Requirement analysis and scope finalization",
    "W2-W3: DB design and Django setup",
    "W3-W4: Core modules (auth, medicine, cart)",
    "W4-W5: Prescription + checkout + payment integration",
    "W5-W6: Admin panel + order management + billing",
    "W6-W7: Testing, bug fixing, documentation",
    "W7-W8: Final demo preparation and submission",
    "Use this timeline to draw a hand-written Gantt chart if required.",
    "",
    "Conclusion",
    "MediWay execution aligns with Hybrid SDLC by combining planned architecture and iterative enhancement.",
    "Risk prioritization, role planning, and leadership choices demonstrate practical software project management for a real Django project.",
]


def build_odt():
    with zipfile.ZipFile(BASE_ODT, "r") as zin:
        content_xml = zin.read("content.xml")

    root = ET.fromstring(content_xml)
    office_text = root.find(".//office:text", NS)
    if office_text is None:
        raise RuntimeError("office:text node not found in content.xml")

    office_text.clear()

    for line in content_lines:
        p = ET.SubElement(office_text, f"{{{NS['text']}}}p")
        p.set(f"{{{NS['text']}}}style-name", "P13")
        p.text = line

    new_content = ET.tostring(root, encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(BASE_ODT, "r") as zin, zipfile.ZipFile(OUT_ODT, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "content.xml":
                data = new_content
            zout.writestr(info, data)


if __name__ == "__main__":
    build_odt()
    print(f"Created: {OUT_ODT.resolve()}")

