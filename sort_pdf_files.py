#!/usr/bin/env python3
"""
PDF Content Analyzer

This script scans through PDF files in a directory, extracts their content,
and identifies potentially relevant information such as:
- Document title
- Author
- Creation date
- Keywords
- Common important terms
"""
import re
import PyPDF2
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from collections import Counter
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Common important terms to look for in documents
IMPORTANT_TERMS = [
    'confidential', 'contract', 'agreement', 'invoice', 'receipt',
    'report', 'financial', 'statement', 'tax', 'id', 'ssn', 'personal',
    'private', 'sensitive', 'proposal', 'nda', 'terms', 'conditions'
]

class PDFAnalyzer:
    def __init__(self, search_terms: Optional[List[str]] = None):
        """
        Initialize the PDF analyzer.
        
        Args:
            search_terms: Optional list of terms to search for in documents
        """
        self.search_terms = search_terms or IMPORTANT_TERMS
        self.term_pattern = re.compile(
            r'\b(' + '|'.join(map(re.escape, self.search_terms)) + r')\b',
            re.IGNORECASE
        )
    
    def extract_text_from_pdf(self, pdf_path: Union[str, Path]) -> str:
        """Extract text content from a PDF file."""
        try:
            with pdf_path.open('rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n'
                return text.strip()
        except Exception as e:
            logger.error(f"Error reading {pdf_path}: {str(e)}")
            return ""
    
    def analyze_pdf(self, pdf_path: Union[str, Path]) -> Dict:
        """Analyze a PDF file and extract relevant information."""
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            return {
                'status': 'error',
                'message': f'File not found: {pdf_path}'
            }
        
        file_info = {
            'filename': pdf_path.name,
            'filepath': str(pdf_path.absolute()),
            'size_mb': pdf_path.stat().st_size / (1024 * 1024),
            'metadata': {},
            'found_terms': [],
            'page_count': 0,
            'has_text': False
        }
        
        try:
            with pdf_path.open('rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Extract metadata
                if reader.metadata:
                    file_info['metadata'] = {
                        'title': getattr(reader.metadata, 'title', None),
                        'author': getattr(reader.metadata, 'author', None),
                        'creator': getattr(reader.metadata, 'creator', None),
                        'producer': getattr(reader.metadata, 'producer', None),
                        'creation_date': getattr(reader.metadata, 'creation_date', None),
                        'modification_date': getattr(reader.metadata, '/ModDate', None)
                    }
                
                # Extract text and analyze content
                text = self.extract_text_from_pdf(pdf_path)
                file_info['has_text'] = bool(text.strip())
                file_info['page_count'] = len(reader.pages)
                
                # Search for important terms
                if text:
                    found = set(self.term_pattern.findall(text.lower()))
                    file_info['found_terms'] = sorted(list(found))
                    
                    # Extract potential title (first non-empty line)
                    first_lines = [line.strip() for line in text.split('\n') if line.strip()]
                    if first_lines:
                        file_info['potential_title'] = first_lines[0][:200]  # Limit title length
                
                return file_info
                
        except Exception as e:
            logger.error(f"Error analyzing {pdf_path}: {str(e)}")
            file_info['status'] = 'error'
            file_info['message'] = str(e)
            return file_info

def scan_directory(directory: Path, recursive: bool = True) -> List[Dict]:
    """
    Scan a directory for PDF files and analyze them.
    
    Args:
        directory: Directory path to scan
        recursive: Whether to scan subdirectories
        
    Returns:
        List of analysis results for each PDF file
    """
    analyzer = PDFAnalyzer()
    results = []
    
    try:
        if not directory.exists() or not directory.is_dir():
            logger.error(f"Directory not found: {directory}")
            return []
            
        # Get all PDF files in directory
        pattern = '**/*.pdf' if recursive else '*.pdf'
        pdf_files = list(directory.glob(pattern))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {directory}")
            return []
            
        logger.info(f"Found {len(pdf_files)} PDF files to analyze...")
        
        # Analyze each PDF
        for pdf_file in pdf_files:
            logger.info(f"Analyzing: {pdf_file}")
            result = analyzer.analyze_pdf(pdf_file)
            results.append(result)
            
    except Exception as e:
        logger.error(f"Error scanning directory {directory}: {str(e)}")
    
    return results

def generate_report(results: List[Dict], output_file: Path = Path('pdf_analysis_report.txt')) -> None:
    """Generate a text report from the analysis results."""
    if not results:
        logger.warning("No results to generate report")
        return
        
    output_path = Path(output_file)
    try:
        with output_path.open('w', encoding='utf-8') as f:
            f.write("PDF Analysis Report\n")
            f.write("=" * 50 + "\n\n")
            
            for i, result in enumerate(results, 1):
                f.write(f"{i}. {result.get('filename', 'Unknown')}\n")
                f.write(f"   Path: {result.get('filepath', 'N/A')}\n")
                f.write(f"   Size: {result.get('size_mb', 0):.2f} MB\n")
                f.write(f"   Pages: {result.get('page_count', 0)}\n")
                
                # Add metadata
                meta = result.get('metadata', {})
                if meta.get('title'):
                    f.write(f"   Title: {meta['title']}\n")
                if meta.get('author'):
                    f.write(f"   Author: {meta['author']}\n")
                    
                # Add found terms
                if result.get('found_terms'):
                    f.write(f"   Found terms: {', '.join(result['found_terms'])}\n")
                    
                f.write("\n" + "-" * 50 + "\n\n")
        
        logger.info(f"Report generated: {output_path.absolute()}")
    except Exception as e:
        logger.error(f"Error writing report to {output_path}: {str(e)}")
        raise

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze PDF files in a directory')
    parser.add_argument('directory', help='Directory to scan for PDF files')
    parser.add_argument('--output', '-o', default='pdf_analysis_report.txt',
                      help='Output report file (default: pdf_analysis_report.txt)')
    parser.add_argument('--no-recursive', action='store_false', dest='recursive',
                      help='Do not scan subdirectories')
    
    args = parser.parse_args()
    
    try:
        # Convert to Path objects
        directory = Path(args.directory).expanduser().resolve()
        output_file = Path(args.output).expanduser().resolve()
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Scan directory and analyze PDFs
        results = scan_directory(directory, args.recursive)
        
        if results:
            # Generate report
            generate_report(results, output_file)
            
            # Print summary
            total_files = len(results)
            files_with_terms = sum(1 for r in results if r.get('found_terms'))
            
            print("\nAnalysis complete!")
            print(f"- Total PDFs analyzed: {total_files}")
            print(f"- PDFs with important terms: {files_with_terms}")
            print(f"- Report saved to: {output_file.absolute()}")
        else:
            print("No PDF files were analyzed.")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()