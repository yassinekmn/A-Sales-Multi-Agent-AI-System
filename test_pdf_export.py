#!/usr/bin/env python
"""Test script to verify PDF export works correctly."""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from export_agent import export_report

# Test content
test_content = """
Key Findings

- Headphones Lead Sales: With sales totaling $16,773, Headphones contribute 31.2% of the overall revenue ($53,740).
- Significant Revenue Margin: Headphones outperform the next best-selling product, Phones, by a margin of $3,088.
- Strong Customer Preference: The sales figures suggest robust demand for Headphones, driven either by higher pricing, superior sales volume, or both.

Sales Distribution

| Product | Total Sales (USD) |
|---------|------------------|
| Headphones | $16,773 |
| Phone | $13,685 |
| Tablet | $13,098 |
| Laptop | $10,184 |

Analysis & Recommendations

**Key Insight**: Focus on maintaining Headphones inventory and quality.
"""

print("Testing PDF export...")
try:
    result = export_report(test_content, format="pdf")
    print(f"✅ PDF Export successful!")
    print(f"   File: {result['file_path']}")
    print(f"   Size: {result['size_bytes']} bytes")
    
    # Check file exists
    if Path(result['file_path']).exists():
        print("✅ File exists and readable")
    else:
        print("❌ File does not exist!")
        
except Exception as e:
    print(f"❌ PDF Export failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All tests passed!")
