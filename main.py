from pathlib import Path
from datetime import datetime
import os
import fitz
from docx import Document


def format_file_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 2:
        return f"{round(size / 1024, 2)} KB"
    elif size < 1024 * 3:
        return f"{round(size / (1024 * 2), 2)} MB"
    else:
        return f"{round(size / (1024 * 3), 2)} GB"


def modified_time(timestamp):
    date_time = datetime.fromtimestamp(timestamp)
    return date_time.strftime("%d-%m-%Y %I:%M %p")


def text_txt(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            return content

    except UnicodeDecodeError:
        print("Unicode decode error")

    except PermissionError:
        print("Permission denied")


def text_pdf(file):
    content = []

    doc = fitz.open(file)

    for page in doc:
        content.append(page.get_text())

    return "\n".join(content)


def text_docx(file):
    content = []

    doc = Document(file)

    for paragraph in doc.paragraphs:
        content.append(paragraph.text)

    return "\n".join(content)

def extract_text(file):
    extension = file.suffix.lower()

    if extension == ".txt":
            text = text_txt(file)

    elif extension == ".pdf":
            text = text_pdf(file)

    elif extension == ".docx":
            text = text_docx(file)

    else:
        return None
    return text

def file_details(file):
        if not file.exists() or not file.is_file():
            print("File not found")
            return
        extension = file.suffix.lower()
        paragraph="N/A"    
        pages="N/A" 
        text=extract_text(file)
        if text is None:
             print("unable to extract text")   
             return

                
        words=len(text.split())
        characters=len(text)
        if extension == ".pdf":
            doc=fitz.open(file)
            pages=len(doc)
            doc.close()

                
        if extension == ".docx":
            doc=Document(file)
            paragraph=len(doc.paragraphs)

        details=({
                            "name": file.name,
                            "extension": file.suffix.lower(),
                            "size": format_file_size(file.stat().st_size),
                            "modified": modified_time(file.stat().st_mtime),
                            "Words":words,
                            "characters":characters,
                            "paragraphs":paragraph,
                            "pages":pages})

      

        print("\n--------------------")
        print("Name:", details["name"])
        print("Type:", details["extension"])
        print("Size:", details["size"])
        print("Modified:", details["modified"])
        print("Words:", details["Words"])
        print("Characters:", details["characters"])
        print("Paragraphs:", details["paragraphs"])
        print("Pages:", details["pages"])

  
        

def scan_documents(folder_path):

    folder = Path(folder_path)

    if not folder.exists():
        print("Folder does not exist.")
        return

    if not folder.is_dir():
        print("Provided path is not a folder.")
        return

    supported_extensions = {".pdf", ".docx", ".txt"}

    documents = []

    try:
        for file in folder.rglob("*"):
            if file.is_file() and file.suffix.lower() in supported_extensions:
                documents.append({
                    "name": file.name,
                    "extension": file.suffix.lower(),
                    "size": format_file_size(file.stat().st_size),
                    "modified": modified_time(file.stat().st_mtime)
                })

    except PermissionError:
        print("Permission Denied.")

    print(f"\nDocuments found: {len(documents)}")

    for document in documents:
        print("\n--------------------")
        print("Name:", document["name"])
        print("Type:", document["extension"])
        print("Size:", document["size"])
        print("Modified:", document["modified"])


# ================= MAIN MENU =================

folder_path = input("Enter documents folder path: ")

while True:

    print("\n===== SmartDocumentIntelligence =====")
    print("1. View Folder  Documents")
    print("2. View File Content")
    print("3. View File Details")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        scan_documents(folder_path)

    elif choice == "2":

      f_name = input("Enter File Name: ")
      file = Path(folder_path) / f_name

      if not file.exists() or not file.is_file():
        print("File not found.")
        continue

      text = extract_text(file)

      if text is None:
        print("Unsupported file type.")
        continue

      print("\n========== FILE CONTENT ==========")
      print(text)

        
       


    elif choice == "3":
        print("====File Details====")
        f_name=input("Enter File Name:")
        file=Path(folder_path)/f_name
        file_details(file)

    elif choice == "4":
        print("Exiting SmartDocumentIntelligence...")
        break

    else:
        print("Invalid choice. Please try again.")