import pdfplumber
import json
import re
from typing import Dict, List, Any
import sys
import os

class PDFParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.data = {"pages": []}
        
    def extract_content(self):
        """Main method to extract content from PDF"""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                page_data = self.process_page(page, page_num)
                self.data["pages"].append(page_data)
    
    def process_page(self, page, page_num: int) -> Dict[str, Any]:
        """Process a single page of the PDF"""
        page_data = {
            "page_number": page_num,
            "content": []
        }
        
        # Extract text
        text = page.extract_text()
        if text:
            # Process text to identify sections and paragraphs
            self.process_text_content(text, page_data)
        
        # Extract tables using pdfplumber's built-in method
        tables = page.find_tables()
        for table_num, table in enumerate(tables):
            table_data = self.process_table_with_pdfplumber(table, table_num)
            page_data["content"].append(table_data)
        
        return page_data
    
    def process_text_content(self, text: str, page_data: Dict[str, Any]):
        """Process text content to identify sections and paragraphs"""
        lines = text.split('\n')
        current_section = None
        current_subsection = None
        paragraph_text = []
        
        for line in lines:
            # Identify section headers (heuristic-based)
            if self.is_section_header(line):
                # Save previous paragraph if exists
                if paragraph_text:
                    self.add_paragraph(''.join(paragraph_text), current_section, current_subsection, page_data)
                    paragraph_text = []
                
                current_section = line
                current_subsection = None
            elif self.is_subsection_header(line):
                # Save previous paragraph if exists
                if paragraph_text:
                    self.add_paragraph(''.join(paragraph_text), current_section, current_subsection, page_data)
                    paragraph_text = []
                
                current_subsection = line
            else:
                paragraph_text.append(line + ' ')
        
        # Add the last paragraph
        if paragraph_text:
            self.add_paragraph(''.join(paragraph_text), current_section, current_subsection, page_data)
    
    def is_section_header(self, text: str) -> bool:
        """Heuristic to identify section headers"""
        # Example: Text in all caps or with specific patterns
        if text.isupper() or re.match(r'^#+\s+', text) or len(text) < 50 and text.endswith(':'):
            return True
        return False
    
    def is_subsection_header(self, text: str) -> bool:
        """Heuristic to identify subsection headers"""
        # Example: Text with specific patterns
        if re.match(r'^###+\s+', text) or (len(text) < 100 and text.isupper()):
            return True
        return False
    
    def add_paragraph(self, text: str, section: str, subsection: str, page_data: Dict[str, Any]):
        """Add a paragraph to the page content"""
        if text.strip():
            paragraph = {
                "type": "paragraph",
                "section": section,
                "sub_section": subsection,
                "text": text.strip()
            }
            page_data["content"].append(paragraph)
    
    def process_table_with_pdfplumber(self, table, table_num: int) -> Dict[str, Any]:
        """Process a table using pdfplumber's table extraction"""
        table_data = {
            "type": "table",
            "table_number": table_num,
            "table_data": table.extract()
        }
        return table_data
    
    def save_to_json(self, output_path: str):
        """Save extracted data to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) != 3:
        print("Usage: python pdf_parser.py <input_pdf> <output_json>")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_json = sys.argv[2]
    
    if not os.path.exists(input_pdf):
        print(f"Error: Input file {input_pdf} does not exist")
        sys.exit(1)
    
    parser = PDFParser(input_pdf)
    parser.extract_content()
    parser.save_to_json(output_json)
    print(f"Successfully extracted content to {output_json}")

if __name__ == "__main__":
    main()