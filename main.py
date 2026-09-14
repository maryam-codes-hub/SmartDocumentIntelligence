from pathlib import Path
from datetime import datetime

def format_file_size(size):
    if size<1024:
        return f"{size} B"
    elif size<1024*2:
        return f"{round(size/1024,2)} KB"
    elif size<1024*3:
         return f"{round(size/(1024*2),2)} MB"
    else:
         return f"{round(size/(1024*3),2)} GB"

def modified_time(timestamp):
    date_time=datetime.fromtimestamp(timestamp)
    return date_time.strftime("%d-%m-%Y %I:%M %p")
    
def scan_documents(folder_path):
 
    folder =Path(folder_path)

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
    except:
     print("Permission Denied:")

    print(f"\nDocuments found: {len(documents)}")

    for document in documents:
        print("\n--------------------")
        print("Name:", document["name"])
        print("Type:", document["extension"])
        print("Size:", document["size"])
        print("Modified:", document["modified"])


folder_path = input("Enter documents folder path: ")

scan_documents(folder_path)