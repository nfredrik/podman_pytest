"""
Create a Word document with an embedded image using python-docx-template and Jinja2 templates.

This module provides functionality to generate Word documents by combining a template
(.docx file with Jinja2 syntax) with dynamic content including embedded images.
"""
from pathlib import Path
from typing import Dict, Any, Optional
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_document_from_template(
    template_path: str,
    output_path: str,
    context: Dict[str, Any],
    image_path: Optional[str] = None,
    image_placeholder: str = 'image',
    image_size: Optional[Dict[str, float]] = None
) -> None:
    """
    Generate a Word document by populating a template with provided context and optional image.

    This function takes a Word template with Jinja2 placeholders and generates a new document
    by replacing those placeholders with the provided context values. It can also embed an
    image at a specified placeholder in the template.

    Args:
        template_path: Path to the .docx template file with Jinja2 placeholders
        output_path: Path where the generated document will be saved
        context: Dictionary containing the template variables and their values
        image_path: Optional path to an image file to embed in the document
        image_placeholder: The name of the placeholder in the template where the image should be inserted
        image_size: Optional dictionary with 'width' and/or 'height' in millimeters

    Raises:
        FileNotFoundError: If template or image file is not found
        ValueError: If there's an error processing the template or image

    Example:
        >>> context = {
        ...     'title': 'Sample Report',
        ...     'content': 'This is a sample document with an embedded image.'
        ... }
        >>> generate_document_from_template(
        ...     template_path='template.docx',
        ...     output_path='output/report.docx',
        ...     context=context,
        ...     image_path='image.jpg',
        ...     image_size={'width': 100, 'height': 75}
        ... )
    """
    try:
        # Verify template exists
        template_path = Path(template_path)
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")

        # Load the template
        doc = DocxTemplate(template_path)

        # Process image if provided
        if image_path:
            image_path = Path(image_path)
            if not image_path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Set default size if not provided
            if image_size is None:
                image_size = {'width': 100}  # Default width of 100mm

            # Create InlineImage and add to context
            img = InlineImage(
                doc,
                image_path,
                width=Mm(image_size.get('width')) if 'width' in image_size else None,
                height=Mm(image_size.get('height')) if 'height' in image_size else None
            )
            context[image_placeholder] = img

        # Render the template with context
        doc.render(context)

        # Ensure output directory exists
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the document
        doc.save(output_path)
        logger.info(f"Document successfully generated: {output_path}")

    except Exception as e:
        logger.error(f"Error generating document: {e}")
        raise

def main():
    """Example usage of the document generation function."""
    try:
        # Example context with template variables
        context = {
            'title': 'Sample Document',
            'content': 'This document was generated using python-docx-template.',
            'author': 'Document Generator'
        }

        # Generate the document
        generate_document_from_template(
            template_path='template.docx',
            output_path='output/generated_document.docx',
            context=context,
            image_path='image.jpg',
            image_size={'width': 80, 'height': 60}
        )
    except Exception as e:
        logger.critical(f"Failed to generate document: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()