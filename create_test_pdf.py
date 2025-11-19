#!/usr/bin/env python3
"""Create a test PDF resume for testing the upload functionality."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT

# Read the text resume
with open('test_resume.txt', 'r') as f:
    content = f.read()

# Create PDF
doc = SimpleDocTemplate("test_resume.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Split content into lines
lines = content.split('\n')

for line in lines:
    if line.strip():
        # Determine style based on content
        if line.isupper() and len(line.split()) <= 3:
            # Section headers
            style = ParagraphStyle('Custom', parent=styles['Heading1'], fontSize=14, spaceAfter=6)
        elif line.strip() and not line.startswith(' ') and not line.startswith('-'):
            # Job titles, company names
            style = ParagraphStyle('Custom', parent=styles['Heading2'], fontSize=11, spaceAfter=3)
        else:
            # Regular text
            style = styles['Normal']

        p = Paragraph(line, style)
        story.append(p)
    else:
        story.append(Spacer(1, 0.1*inch))

doc.build(story)
print("✅ Created test_resume.pdf successfully")
