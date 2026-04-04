# 🎯 Web Dashboard Quick Start Guide

## What's New?

Your AI Data Team project now has a **professional web dashboard** that non-technical clients can use without opening a terminal!

## How to Start the Dashboard

### Windows Users
1. Double-click: **`run_dashboard.bat`**
2. Wait for the dashboard to load (usually 5-10 seconds)
3. Your browser opens automatically to: http://localhost:8501

### Mac/Linux Users
```bash
python start_dashboard.py
```
Then open: http://localhost:8501

## Dashboard Features

### 📊 Dashboard Tab
- View key metrics (Total Orders, Revenue, Units Sold, Regions)
- See data table with all sales records
- Visualizations for Sales by Product and Region
- Quick insights about top products and regions

### 🔍 Ask AI Tab
- **Chat-like interface** for non-technical users
- Just type a question like: "Which region sold the most?"
- Get instant AI analysis with professional formatting
- Export results as JSON reports

### 📈 Comparisons Tab
- **Regional Performance** - Compare how different regions are performing
- **Product Comparison** - See which products are selling better
- Export comparison results

### 📄 Reports Tab
- View all previously generated reports
- Download reports in multiple formats
- Clean up old reports

## Files Added/Modified

### New Files Created:
- **`streamlit_app.py`** - Main web application (650+ lines)
- **`run_dashboard.bat`** - Windows starter script
- **`start_dashboard.py`** - Cross-platform starter script

### Updated Files:
- **`requirements.txt`** - Added: streamlit, plotly
- **`README.md`** - Added dashboard setup instructions

## Example Client Workflow

1. **Client double-clicks run_dashboard.bat**
2. **Dashboard opens in browser** (looks professional and modern)
3. **Client navigates to "Dashboard" tab**
   - Sees all their sales metrics at a glance
4. **Client clicks "Ask AI" tab**
   - Types: "Compare our top 3 products"
   - Gets instant analysis with insights
5. **Client clicks "Export"**
   - Downloads report as JSON
6. **Client shows report to stakeholders** - looks professional ✅

## Technical Details

- **Framework**: Streamlit (Python web framework)
- **Charts**: Plotly (interactive visualizations)
- **Backend**: Integrates with existing AI agents
- **No coding needed**: Just point-and-click interface

## URL & Port

- **Local URL**: http://localhost:8501
- **Port**: 8501 (can be changed if needed)

## Stopping the Dashboard

- Press `Ctrl + C` in the terminal/CMD window
- Or close the command window

## Troubleshooting

**Dashboard won't start?**
- Make sure you've installed requirements: `pip install -r requirements.txt`
- Check that .env file is configured with API tokens

**Port already in use?**
- Close other applications using port 8501
- Or modify startup script to use different port

**Data not loading?**
- Verify `sales.csv` exists in the project root
- Check that API tokens are correct in .env

## Next Steps

1. ✅ Install dependencies (done above)
2. Start dashboard with `run_dashboard.bat` or `python start_dashboard.py`
3. Test each tab to ensure it works
4. Show to non-technical users/clients
5. Gather feedback for improvements

---
Created: April 3, 2026
For questions, check `streamlit_app.py` or `README.md`
