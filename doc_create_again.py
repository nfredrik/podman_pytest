"""
Document generation with embedded images using python-docx-template.

This module demonstrates how to create Word documents with embedded images
using Jinja2 templating and python-docx-template.
"""
from pathlib import Path
from typing import Dict, List, Any, Optional

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import jinja2
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_framework_dict(
    template: DocxTemplate,
    name: str,
    description: str,
    height_mm: float = 10.0
) -> Dict[str, Any]:
    """Create a dictionary representing a framework with its image and description.
    
    Args:
        template: The DocxTemplate instance.
        name: Name of the framework (used for the image filename).
        description: Description of the framework.
        height_mm: Height of the image in millimeters.
        
    Returns:
        Dictionary containing the framework's image and description.
    """
    return {
        'image': InlineImage(template, str(Path(f"{name.lower()}.png")), height=Mm(height_mm)),
        'desc': description
    }


def generate_document(
    template_path: str,
    output_path: str,
    image_dir: str = '.',
    output_dir: str = 'output'
) -> None:
    """Generate a Word document with embedded images from a template.
    
    Args:
        template_path: Path to the Word template file.
        output_path: Filename for the output document.
        image_dir: Directory containing the image files.
        output_dir: Directory where the output document will be saved.
        
    Raises:
        FileNotFoundError: If the template file or any image is not found.
        Exception: For other errors during document generation.
    """
    try:
        # Ensure paths are Path objects
        template_path = Path(template_path)
        image_dir = Path(image_dir)
        output_dir = Path(output_dir)
        
        # Check if template exists
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
            
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize template
        template = DocxTemplate(template_path)
        
        # Define framework data
        frameworks_data = [
            ("Django", "The web framework for perfectionists with deadlines"),
            (
                "Zope", 
                "Zope is a leading Open Source Application Server and "
                "Content Management Framework"
            ),
            (
                "Pyramid",
                "Pyramid is a lightweight Python web framework aimed at taking "
                "small web apps into big web apps."
            ),
            (
                "Bottle",
                "Bottle is a fast, simple and lightweight WSGI micro "
                "web-framework for Python"
            ),
            (
                "Tornado",
                "Tornado is a Python web framework and asynchronous networking "
                "library."
            ),
        ]
        
        # Create framework entries with images
        frameworks = [
            create_framework_dict(template, name, desc)
            for name, desc in frameworks_data
        ]
        
        # Prepare context
        context = {
            'myimage': InlineImage(template, str(image_dir / "python_logo.png"), width=Mm(20)),
            'myimageratio': InlineImage(
                template, 
                str(image_dir / "python_jpeg.jpg"), 
                width=Mm(30), 
                height=Mm(60)
            ),
            'frameworks': frameworks
        }
        
        # Render and save with autoescape=True
        #jinja_env = jinja2.Environment(autoescape=True)
        #template.render(context, jinja_env)
        template.render(context)

        # Save the output
        output_file = output_dir / output_path
        template.save(output_file)
        logger.info(f"Document successfully generated: {output_file}")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error generating document: {e}", exc_info=True)
        raise


def main() -> None:
    """Main function to demonstrate document generation."""
    try:
        generate_document(
            template_path="inline_image_tpl.docx",
            output_path="inline_image.docx",
            image_dir=".",
            output_dir="output"
        )
    except Exception as e:
        logger.critical("Failed to generate document", exc_info=True)
        raise


if __name__ == "__main__":
    main()