import os
import shutil
from datetime import datetime
from reportlab.pdfgen import canvas

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "file_manager")
BASE_DIR = os.path.abspath(BASE_DIR)

def ensure_folders():
    folders = ["reports", "documents", "images", "pdfs"]
    for folder in folders:
        os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

ensure_folders()

# ------------------- SAVE TXT -------------------
def save_text_report(content, filename=None):
    ensure_folders()

    if not filename:
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    file_path = os.path.join(BASE_DIR, "reports", filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path

# ------------------- SAVE WORD -------------------
def save_word(content, filename=None):
    from docx import Document

    ensure_folders()

    if not filename:
        filename = f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"

    file_path = os.path.join(BASE_DIR, "documents", filename)

    doc = Document()
    doc.add_paragraph(content)
    doc.save(file_path)

    return file_path

# ------------------- SAVE PDF FROM TEXT -------------------
def save_pdf(content, filename=None):
    ensure_folders()

    if not filename:
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    file_path = os.path.join(BASE_DIR, "pdfs", filename)

    # Generate PDF using ReportLab
    c = canvas.Canvas(file_path)
    text_object = c.beginText(40, 800)
    text_object.setFont("Helvetica", 12)

    for line in content.split("\n"):
        text_object.textLine(line)

    c.drawText(text_object)
    c.save()

    return file_path


# ------------------- SAVE IMAGE -------------------
def save_image(image_bytes, filename=None):
    ensure_folders()

    if not filename:
        filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    file_path = os.path.join(BASE_DIR, "images", filename)

    with open(file_path, "wb") as f:
        f.write(image_bytes)

    return file_path

# ------------------- ORGANIZE FOLDER -------------------
def organize_folder(folder_path):
    if not os.path.exists(folder_path):
        return "❌ Folder does not exist."

    categories = {
        "Documents": [".txt", ".docx", ".doc", ".ppt", ".pptx", ".xlsx", ".csv"],
        "Images": [".png", ".jpg", ".jpeg", ".gif"],
        "PDFs": [".pdf"],
        "Videos": [".mp4", ".avi", ".mov"],
        "Others": []
    }

    count = 0

    for filename in os.listdir(folder_path):
        src = os.path.join(folder_path, filename)
        if os.path.isdir(src):
            continue

        ext = os.path.splitext(filename)[1].lower()
        moved = False

        for category, ext_list in categories.items():
            if ext in ext_list:
                dest_folder = os.path.join(folder_path, category)
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(src, os.path.join(dest_folder, filename))
                moved = True
                count += 1
                break

        if not moved:
            dest = os.path.join(folder_path, "Others")
            os.makedirs(dest, exist_ok=True)
            shutil.move(src, os.path.join(dest, filename))
            count += 1

    return f" Organized {count} files!"
