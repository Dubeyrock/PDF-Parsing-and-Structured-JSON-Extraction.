# PDF Parser and JSON Extractor

This Python program extracts content from PDF files and converts it to a structured JSON format.


Project Folder Structure
Create this folder structure in VS Code:

text
pdf-parser-project/
├── src/
│   └── pdf_parser.py
├── input/
│   └── [PDF file(s)]
├── output/
│   └── [JSON output]
├── requirements.txt
└── README.md


## Installation

1. Clone or download this repository
2. Install dependencies:

pip install -r requirements.txt

## Usage

Run the script with the following command:

Replace `pdf-parser-project\input\[Fund Factsheet - May]360ONE-MF-May 2025.pdf.pdf` with your input PDF file and `output.json` with your desired output file name.

## Features

- Extracts text content with section hierarchy
- Identifies and extracts tables
- Outputs structured JSON with page-level organization
- Preserves document hierarchy (sections, subsections)

## Dependencies

- pdfplumber: For text extraction
- camelot-py: For table extraction
- pandas: For data manipulation


### How to Run
Place your PDF file in the input folder

Run the script:

bash
python src/pdf_parser.py input/your_pdf_file.pdf output/extracted_data.json

Tips for Success
Test with the provided PDF: Make sure your code works with the sample PDF provided in the assignment

Handle edge cases: Consider PDFs with different structures, empty pages, etc.

Improve section detection: You might need to customize the header detection logic based on the specific PDF structure

Add error handling: Make your code robust with proper exception handling

Document your code: Add comments explaining your approach and decisions

Next Steps
Implement the basic structure as shown

Test with the provided PDF

Refine the section detection algorithms

Add support for charts (you might need to use additional libraries like OpenCV or pytesseract)

Make the code more robust and add error handling