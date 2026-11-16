
import os
import zipfile

# Project evidence storage directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "app",
    "static",
    "evidence"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


DATASETS = {
    "deleted_documents.zip": {
        "README.txt": """
ForenQuest - Deleted Files Practice Dataset

This is a synthetic training dataset.

Scenario:
An employee allegedly deleted important documents.

Examine the records to identify deleted files.

All information is fictional.
""",
        "deleted_file_records.csv": """filename,file_type,status,original_location
annual_report.pdf,PDF,Deleted,Documents
employee_list.docx,DOCX,Deleted,Documents
office_photo.jpg,JPG,Deleted,Pictures
budget_summary.pdf,PDF,Existing,Documents
"""
    },

    "hidden_files.zip": {
        "README.txt": """
ForenQuest - Hidden Evidence Practice Dataset

This is a synthetic training dataset.

Scenario:
Investigators suspect that a user concealed
important files on a computer.

Examine the provided records.
""",
        "hidden_files.csv": """filename,location,attribute
secret_notes.txt,C:/Users/Student/Documents,Hidden
backup_data.txt,C:/Users/Student/AppData,Hidden
normal_report.txt,C:/Users/Student/Documents,Normal
archive_old.zip,C:/Users/Student/Desktop,Hidden
"""
    },

    "file_signatures.zip": {
        "README.txt": """
ForenQuest - Hex Investigation Practice Dataset

This is a synthetic training dataset.

Scenario:
Some files have incorrect extensions.

Compare their reported extensions with
their hexadecimal file signatures.
""",
        "file_signatures.txt": """
Filename: image_sample.jpg
Extension: JPG
Signature: FF D8 FF
Expected type: JPEG image

Filename: document_sample.pdf
Extension: PDF
Signature: 25 50 44 46
Expected type: PDF document

Filename: archive_sample.zip
Extension: TXT
Signature: 50 4B 03 04
Expected type: ZIP archive

Filename: picture_sample.png
Extension: PNG
Signature: 89 50 4E 47 0D 0A 1A 0A
Expected type: PNG image
"""
    },

    "usb_artifacts.zip": {
        "README.txt": """
ForenQuest - USB Investigation Practice Dataset

This is a synthetic training dataset.

Scenario:
A confidential file may have been copied
to an external USB device.

Examine the mock Windows artifacts.
""",
        "USBSTOR.csv": """device_name,serial_number,connection_status
Kingston USB,USB123456,Connected
SanDisk USB,SD987654,Disconnected
Generic Flash Drive,GF456789,Connected
""",
        "setupapi_log.txt": """
Synthetic Windows SetupAPI log

2026-10-01 09:15 - Kingston USB connected
2026-10-01 10:30 - SanDisk USB connected
2026-10-02 14:20 - Kingston USB disconnected

All entries are fictional training records.
"""
    }
}


for filename, files in DATASETS.items():

    output_path = os.path.join(OUTPUT_DIR, filename)

    with zipfile.ZipFile(
        output_path,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as archive:

        for internal_name, content in files.items():
            archive.writestr(internal_name, content.strip())

    print(f"Created: {filename}")


print("\nAll four forensic practice datasets generated.")
