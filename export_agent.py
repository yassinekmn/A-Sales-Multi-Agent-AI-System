# export_agent.py
"""Export Agent - Generates reports in multiple formats (PDF, Excel, JSON, HTML)."""

import os
import json
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors

from config import AgentType, SystemConfig
from utils.logger import get_logger
from utils.errors import AgentExecutionError

logger = get_logger(__name__)


def export_report(content: str, format: str = "json", filename: str = None, title: str = None) -> dict:
    """
    Export report content in specified format.
    
    Args:
        content: Report content to export
        format: Output format ('json', 'txt', 'html', 'pdf')
        filename: Optional custom filename (without extension)
        title: Optional title for the report (used in PDF)
        
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
            # If we have a title, generate filename from it
            if title:
                # Convert title to filename-friendly format
                clean_title = title.lower().strip()
                clean_title = clean_title.replace('?', '').replace('!', '')
                clean_title = clean_title.replace(' ', '-')[:50]  # Max 50 chars
                filename = clean_title or filename
        
        file_path = exports_dir / f"{filename}.{format}"
        
        # Export based on format
        if format.lower() == 'json':
            _export_json(content, file_path)
        elif format.lower() == 'txt':
            _export_txt(content, file_path)
        elif format.lower() == 'html':
            _export_html(content, file_path)
        elif format.lower() == 'pdf':
            _export_pdf(content, file_path, title=title)
        
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


def _export_pdf(content: str, file_path: Path, title: str = None) -> None:
    """Export as PDF format using ReportLab with professional styling."""
    import re
    from reportlab.pdfbase.pdfmetrics import registerFont
    from reportlab.pdfbase.ttfonts import TTFont
    
    try:
        pdf_path = str(file_path).replace('.pdf', '') + '.pdf'
        
        # Create PDF with custom footer
        from reportlab.platypus import PageTemplate, BaseDocTemplate, Frame
        
        class NumberedCanvas:
            def __init__(self, *args, **kwargs):
                self.num_pages = 0
                
        class FooterPageTemplate(PageTemplate):
            def __init__(self, title_text):
                self.title_text = title_text
                
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch,
            title=title or "AI Data Team Report"
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Professional title style - simpler, no color
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=28
        )
        
        # Subtitle/separator style
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#999999'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica',
            leading=12
        )
        
        # Section heading style - centered
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            leading=14,
            alignment=TA_CENTER
        )
        
        # Body style - centered
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            leading=16,
            alignment=TA_CENTER
        )
        
        # Add professional title
        if title:
            # Clean title - remove markdown
            clean_title = title.replace('**', '').replace('##', '').replace('#', '').strip()
            story.append(Paragraph(clean_title, title_style))
        else:
            story.append(Paragraph("📊 Data Analysis Report", title_style))
        
        # Add horizontal line
        from reportlab.platypus import HRFlowable
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#667eea')))
        
        story.append(Spacer(1, 0.15*inch))
        
        # Clean up content
        cleaned_content = content
        cleaned_content = re.sub(r'^-{5,}', '', cleaned_content, flags=re.MULTILINE)
        cleaned_content = re.sub(r'^_{5,}', '', cleaned_content, flags=re.MULTILINE)
        cleaned_content = re.sub(r'--$', '', cleaned_content)
        cleaned_content = cleaned_content.strip()
        
        # Split and process sections
        sections = cleaned_content.split('\n\n')
        
        for section in sections:
            if not section.strip():
                continue
            
            section = section.strip()
            
            # Format markdown
            section = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', section)
            section = re.sub(r'_(.+?)_', r'<i>\1</i>', section)
            
            # Detect and format headers
            if section.startswith('###'):
                clean_section = re.sub(r'^###\s+', '', section).strip()
                story.append(Paragraph(clean_section, heading_style))
            elif section.startswith('<b>') and section.endswith('</b>') and '\n' not in section and len(section) < 150:
                story.append(Paragraph(section, heading_style))
            # Handle bullet points
            elif section.startswith('- '):
                bullets = section.split('\n')
                for bullet in bullets:
                    if bullet.strip().startswith('- '):
                        bullet_text = bullet.strip()[2:]
                        story.append(Paragraph(f"• {bullet_text}", body_style))
            # Regular body text
            else:
                story.append(Paragraph(section, body_style))
            
            story.append(Spacer(1, 0.08*inch))
        
        # Add footer with date
        story.append(Spacer(1, 0.4*inch))
        
        # Footer line
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#eeeeee')))
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#aaaaaa'),
            alignment=TA_CENTER,
            fontName='Helvetica',
            leading=10
        )
        
        timestamp_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')} • AI Data Team"
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(timestamp_text, footer_style))
        
        # Build PDF
        doc.build(story)
        logger.info(f"PDF created successfully at: {pdf_path}")
        
    except Exception as e:
        logger.error(f"PDF export error: {str(e)}", exc_info=True)
        raise
