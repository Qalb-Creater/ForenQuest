
CASES = [
    {
        "id": "deleted-files",
        "title": "Deleted Files Investigation",
        "level": "Beginner",
        "category": "File System Forensics",
        "description": (
            "Investigate a forensic disk image to recover deleted "
            "PDF, DOCX and JPG files."
        ),
        "scenario": (
            "An employee allegedly deleted important documents "
            "before leaving an organization. Your task is to examine "
            "the forensic image and identify recoverable evidence."
        ),
        "filesystem": "NTFS",
        "artifacts": [
            "Deleted PDF documents",
            "Deleted DOCX documents",
            "Deleted JPG images",
            "Recycle Bin artifacts",
            "Unallocated space"
        ],
        "objectives": [
            "Understand deleted file records.",
            "Examine NTFS file-system structures.",
            "Identify files in unallocated space.",
            "Recover deleted evidence."
        ],
        "tools": [
            "Autopsy",
            "FTK Imager",
            "PhotoRec"
        ]
    },
    {
        "id": "hidden-evidence",
        "title": "Hidden Evidence Investigation",
        "level": "Intermediate",
        "category": "File System Forensics",
        "description": (
            "Find hidden files, folders, partitions and suspicious "
            "file-system entries."
        ),
        "scenario": (
            "Investigators suspect that a user concealed important "
            "files on a computer. Examine the provided evidence to "
            "identify hidden data."
        ),
        "filesystem": "NTFS",
        "artifacts": [
            "Hidden files and folders",
            "Unallocated space",
            "Hidden partitions",
            "Suspicious file-system entries"
        ],
        "objectives": [
            "Identify hidden files and directories.",
            "Examine partition structures.",
            "Inspect file-system entries.",
            "Document suspicious findings."
        ],
        "tools": [
            "Autopsy",
            "The Sleuth Kit",
            "TestDisk"
        ]
    },
    {
        "id": "hex-investigation",
        "title": "Hex Investigation",
        "level": "Intermediate",
        "category": "File Analysis",
        "description": (
            "Analyze file signatures, headers, extensions and "
            "embedded file content."
        ),
        "scenario": (
            "A suspicious collection of files has been discovered. "
            "Some files have incorrect extensions or damaged headers. "
            "Analyze their hexadecimal structure."
        ),
        "filesystem": "File-level analysis",
        "artifacts": [
            "Files with incorrect extensions",
            "Modified file headers",
            "Corrupted files",
            "Embedded file content"
        ],
        "objectives": [
            "Understand hexadecimal representation.",
            "Identify file signatures and magic bytes.",
            "Compare extensions with actual file types.",
            "Identify embedded or corrupted content."
        ],
        "tools": [
            "HxD",
            "WinHex",
            "ImHex"
        ]
    },
    {
        "id": "usb-investigation",
        "title": "USB Investigation",
        "level": "Advanced",
        "category": "Windows Artifact Forensics",
        "description": (
            "Investigate USB connection history and Windows "
            "artifacts related to external storage devices."
        ),
        "scenario": (
            "A confidential file may have been copied to an external "
            "USB device. Examine Windows artifacts to reconstruct "
            "the device activity."
        ),
        "filesystem": "Windows artifacts and NTFS",
        "artifacts": [
            "USB device connection records",
            "Windows Registry artifacts",
            "File activity evidence",
            "Device identification information"
        ],
        "objectives": [
            "Identify connected USB devices.",
            "Examine relevant Registry artifacts.",
            "Analyze device and file activity.",
            "Build an evidence-based activity timeline."
        ],
        "tools": [
            "Autopsy",
            "KAPE",
            "Registry Explorer",
            "MFTECmd"
        ]
    }
]
