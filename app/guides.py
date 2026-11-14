
GUIDES = [
    {
        "case_id": "deleted-files",
        "title": "Deleted Files Investigation Guide",
        "introduction": (
            "Learn how to examine deleted files in an NTFS "
            "forensic image and identify recoverable evidence."
        ),
        "tools": ["FTK Imager", "Autopsy", "PhotoRec"],
        "prerequisites": [
            "Basic understanding of files and folders.",
            "Familiarity with NTFS file systems.",
            "A forensic image or practice evidence package."
        ],
        "steps": [
            {
                "title": "Prepare the forensic evidence",
                "instructions": (
                    "Open the supplied forensic image using your "
                    "forensic imaging or examination software. "
                    "Keep the original evidence unchanged."
                )
            },
            {
                "title": "Examine the file system",
                "instructions": (
                    "Use Autopsy to examine the NTFS file system. "
                    "Review the directory structure and identify "
                    "available file-system information."
                )
            },
            {
                "title": "Locate deleted files",
                "instructions": (
                    "Review deleted-file entries and the Recycle Bin. "
                    "Look for deleted PDF, DOCX and JPG files."
                )
            },
            {
                "title": "Examine unallocated space",
                "instructions": (
                    "Inspect unallocated space for traces of deleted "
                    "file content. Use PhotoRec where appropriate "
                    "to attempt file recovery."
                )
            },
            {
                "title": "Record your findings",
                "instructions": (
                    "Record the file names, file types, locations "
                    "and recovery results. Preserve relevant evidence "
                    "details for your investigation report."
                )
            }
        ],
        "questions": [
            "What is a deleted file?",
            "What is unallocated space?",
            "Why can deleted files sometimes be recovered?",
            "What information did you recover from the evidence?"
        ]
    },
    {
        "case_id": "hidden-evidence",
        "title": "Hidden Evidence Investigation Guide",
        "introduction": (
            "Learn how to locate hidden files, folders, partitions "
            "and suspicious file-system entries."
        ),
        "tools": ["Autopsy", "The Sleuth Kit", "TestDisk"],
        "prerequisites": [
            "Basic knowledge of disk partitions.",
            "Understanding of files and directories.",
            "A forensic image or practice evidence package."
        ],
        "steps": [
            {
                "title": "Load the evidence",
                "instructions": (
                    "Open the forensic image in Autopsy and "
                    "review its available volumes and partitions."
                )
            },
            {
                "title": "Inspect hidden files and folders",
                "instructions": (
                    "Examine the directory structure and look for "
                    "files or folders marked as hidden."
                )
            },
            {
                "title": "Examine file-system entries",
                "instructions": (
                    "Use The Sleuth Kit to inspect relevant "
                    "file-system metadata and entries. Compare "
                    "suspicious entries with normal files."
                )
            },
            {
                "title": "Review partition information",
                "instructions": (
                    "Use TestDisk to examine partition information "
                    "and identify partitions that may not be "
                    "normally visible."
                )
            },
            {
                "title": "Document suspicious evidence",
                "instructions": (
                    "Record the location, metadata and characteristics "
                    "of each suspicious file or partition. "
                    "Do not assume hidden means malicious."
                )
            }
        ],
        "questions": [
            "What is a hidden file?",
            "How can a file be marked as hidden?",
            "What is a disk partition?",
            "Why should investigators examine file-system metadata?"
        ]
    },
    {
        "case_id": "hex-investigation",
        "title": "Hex Investigation Guide",
        "introduction": (
            "Learn how to examine hexadecimal data, file signatures "
            "and files with incorrect extensions."
        ),
        "tools": ["HxD", "WinHex", "ImHex"],
        "prerequisites": [
            "Basic understanding of binary and hexadecimal values.",
            "Knowledge of common file extensions.",
            "Sample files prepared for examination."
        ],
        "steps": [
            {
                "title": "Select a sample file",
                "instructions": (
                    "Open a supplied sample file in a hex editor. "
                    "Work on a copy rather than modifying the original."
                )
            },
            {
                "title": "Examine the hexadecimal header",
                "instructions": (
                    "Inspect the beginning of the file and identify "
                    "its header bytes."
                )
            },
            {
                "title": "Identify the file signature",
                "instructions": (
                    "Compare the observed header bytes with known "
                    "file signatures to determine the likely file type."
                )
            },
            {
                "title": "Compare the extension",
                "instructions": (
                    "Compare the actual file signature with the "
                    "file extension. Identify any mismatch."
                )
            },
            {
                "title": "Record the analysis",
                "instructions": (
                    "Document the observed bytes, expected signature, "
                    "file extension and your conclusion. Note any "
                    "corruption or embedded content you identify."
                )
            }
        ],
        "questions": [
            "What is hexadecimal representation?",
            "What is a file signature?",
            "Why can a file extension be misleading?",
            "What is the difference between a file header and its extension?"
        ]
    },
    {
        "case_id": "usb-investigation",
        "title": "USB Investigation Guide",
        "introduction": (
            "Learn how to examine Windows artifacts to investigate "
            "USB device connections and related file activity."
        ),
        "tools": [
            "Autopsy",
            "KAPE",
            "Registry Explorer",
            "MFTECmd"
        ],
        "prerequisites": [
            "Basic knowledge of Windows operating systems.",
            "Understanding of Windows Registry.",
            "A prepared Windows forensic evidence package."
        ],
        "steps": [
            {
                "title": "Prepare Windows evidence",
                "instructions": (
                    "Open the supplied forensic evidence package. "
                    "Identify the available Windows artifacts and "
                    "preserve the original evidence."
                )
            },
            {
                "title": "Identify USB device artifacts",
                "instructions": (
                    "Use Registry Explorer to examine relevant "
                    "Windows Registry information about connected "
                    "USB storage devices."
                )
            },
            {
                "title": "Examine Windows artifacts",
                "instructions": (
                    "Use KAPE to collect or process the relevant "
                    "Windows artifacts from a forensic working copy."
                )
            },
            {
                "title": "Analyze file-system activity",
                "instructions": (
                    "Use MFTECmd to examine available NTFS metadata "
                    "and identify relevant file activity."
                )
            },
            {
                "title": "Build an investigation timeline",
                "instructions": (
                    "Compare device information and file-system "
                    "timestamps. Record what the artifacts support "
                    "and note any limitations."
                )
            }
        ],
        "questions": [
            "What is a USB device artifact?",
            "Where can Windows store USB connection information?",
            "What is the Windows Registry?",
            "How can investigators correlate device and file activity?"
        ]
    }
]
