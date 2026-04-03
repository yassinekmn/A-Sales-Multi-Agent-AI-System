# export_agent.py
"""Export Agent - Generates reports in multiple formats (PDF, Excel, JSON, HTML)."""

import os
import json
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER

from config import AgentType, SystemConfig
from utils.logger import get_logger
from utils.errors import AgentExecutionError

logger = get_logger(__name__)


def export_report(content: str, format: str = "json", filename: str = None) -> dict:
    """
    Export report content in specified format.
    
    Args:
        content: Report content to export
        format: Output format ('json', 'txt', 'html')
        filename: Optional custom filename (without extension)
        
    Returns:
        Dictionary with file path and metadata
        
    Raises:
        AgentExecutionError: If export fails
    """
    try:
        if not content:
            raise ValueError("No content to export")
        
        # Validate format
        valid_formats = ['json', 'txt', 'html', 'pdf']
        if format.lower() not in valid_formats:
            raise ValueError(f"Format must be one of: {', '.join(valid_formats)}")
        
        logger.info(f"Exporting report to format: {format}")
        
        # Create exports directory if it doesn't exist
        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        
        # Generate filename
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}"
        
        file_path = exports_dir / f"{filename}.{format}"
        
        # Export based on format
        if format.lower() == 'json':
            _export_json(content, file_path)
        elif format.lower() == 'txt':
            _export_txt(content, file_path)
        elif format.lower() == 'html':
            _export_html(content, file_path)
        elif format.lower() == 'pdf':
            _export_pdf(content, file_path)
        
        logger.info(f"Report exported successfully: {file_path}")
        
        return {
            "success": True,
            "file_path": str(file_path),
            "format": format,
            "size_bytes": file_path.stat().st_size,
            "created_at": datetime.now().isoformat(),
            "agent": "export_agent"
        }
        
    except Exception as e:
        logger.error(f"Export failed: {str(e)}", exc_info=True)
        raise AgentExecutionError("export_agent", str(e), original_error=e)


def _export_json(content: str, file_path: Path) -> None:
    """Export as JSON format."""
    data = {
        "report": content,
        "generated_at": datetime.now().isoformat(),
        "format": "json"
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _export_txt(content: str, file_path: Path) -> None:
    """Export as plain text format."""
    header = f"{'='*60}\n"
    header += f"REPORT - Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    header += f"{'='*60}\n\n"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
        f.write(f"\n\n{'='*60}\n")


def _export_html(content: str, file_path: Path) -> None:
    """Export as HTML format."""
    # Convert markdown-style formatting to basic HTML
    html_content = content.replace('\n', '<br>\n')
    html_content = html_content.replace('**', '<strong>').replace('**', '</strong>')
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Data Team Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{
            color: #333;
        }}
        .header {{
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #007bff;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Data Team Report</h1>
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        <div class="content">
            {html_content}
        </div>
    </div>
</body>
</html>"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)


def _export_pdf(content: str, file_path: Path) -> None:
    """Export as PDF format using ReportLab."""
    import re
    
    # Create PDF document
    pdf_path = str(file_path).replace('.pdf', '') + '.pdf'
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
    )
    
    # Container for the 'Flowable' objects
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#007bff',
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=12,
        textColor='#333333',
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    # Add title
    story.append(Paragraph("AI Data Team Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Add timestamp
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    story.append(Paragraph(timestamp_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Convert markdown formatting to HTML-like format for ReportLab
    # Replace **text** with <b>text</b>
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
    
    # Split by double newlines to identify sections
    sections = html_content.split('\n\n')
    
    for section in sections:
        if section.strip():
            # Clean up the section
            clean_section = section.strip()
            
            # Add as paragraph
            if clean_section:
                story.append(Paragraph(clean_section, styles['BodyText']))
                story.append(Spacer(1, 0.1*inch))
    
    # Add footer
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph('_' * 60, styles['Normal']))
    
    # Build PDF
    doc.build(story)
