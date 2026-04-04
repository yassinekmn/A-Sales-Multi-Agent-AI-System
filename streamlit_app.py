"""
Streamlit Web Dashboard for AI Data Team
Interactive interface for non-technical users to analyze sales data using AI agents.
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path

# Import AI agents
from data_analyst_agent import analyze_data
from insight_generator_agent import generate_insights
from report_writer_agent import generate_report
from planner_agent import plan_tasks
from export_agent import export_report
from comparison_agent import compare_regions, compare_products
from utils.logger import get_logger

logger = get_logger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="AI Data Team Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DEMO MODE DETECTION
# ============================================================================
def is_demo_mode():
    """Check if API tokens are configured."""
    required_tokens = [
        "ANALYST_GITHUB_TOKEN",
        "PLANNER_GITHUB_TOKEN",
        "INSIGHT_GITHUB_TOKEN",
        "REPORT_GITHUB_TOKEN"
    ]
    return not all(os.getenv(token) and os.getenv(token) != "ghp_your_token_here" for token in required_tokens)

# Sample demo data
DEMO_ANALYSIS = {
    "Which region sold the most units?": "Based on the sales data analysis:\n\n📊 **Regional Performance:**\nRegion A: 1,250 units sold ($45,000 in revenue)\nRegion B: 980 units sold ($38,500 in revenue)\nRegion C: 750 units sold ($28,000 in revenue)\n\n🏆 **Winner:** Region A with 1,250 units - the clear market leader with 32% of total units sold.",
    "What are the top 3 products by revenue?": "📊 **Top 3 Products by Revenue:**\n\n1. 🥇 Premium Widget - $52,000 (35% of total revenue)\n   Average sale: $1,300\n   Units sold: 40\n\n2. 🥈 Standard Device - $42,000 (28% of total revenue)\n   Average sale: $1,050\n   Units sold: 40\n\n3. 🥉 Basic Tool - $35,000 (23% of total revenue)\n   Average sale: $875\n   Units sold: 40",
    "Show me the average sale price by region": "💰 **Average Sale Price by Region:**\n\nRegion A: $1,200 average per transaction\nRegion B: $1,100 average per transaction\nRegion C: $950 average per transaction\n\n📈 Region A has the highest average transaction value, indicating strong customer purchasing power or premium product selection in that market."
}

# Initialize session state for storing analysis results
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = is_demo_mode()

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .metric-card strong {
        color: #ffffff;
        font-size: 1.05em;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #28a745;
        color: #155724;
        padding: 12px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Demo mode banner at top
if st.session_state.demo_mode:
    st.warning("🎬 **DEMO MODE** - Using sample data and pre-computed results. Configure `.env` file for live AI analysis.")

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    # Demo mode indicator
    if st.session_state.demo_mode:
        st.warning("🎬 **DEMO MODE ACTIVE**\nAPI tokens not configured. Using sample data.")
        st.markdown("""
        To use live AI analysis:
        1. Copy `.env.example` to `.env`
        2. Add your GitHub Marketplace API tokens
        3. Restart this app
        
        [Get free tokens →](https://github.com/settings/tokens)
        """)
    else:
        st.success("✅ Live mode - API tokens configured")
    
    st.markdown("---")
    
    mode = st.radio(
        "Select Mode",
        ["📊 Dashboard", "🔍 Ask AI", "📈 Comparisons", "📄 Reports"],
        help="Choose how you want to interact with the AI Data Team"
    )
    
    st.markdown("---")
    
    # Data file selector
    if os.path.exists("sales.csv"):
        st.success("✅ Data loaded: sales.csv")
    else:
        st.error("❌ Data file not found")
    
    st.markdown("---")
    st.markdown("### 📋 About")
    st.info("""
    **AI Data Team** is an autonomous multi-agent system that analyzes your sales data 
    and provides intelligent insights using AI.
    
    🤖 Powered by:
    - Planner Agent
    - Data Analyst Agent
    - Comparison Agent
    - Insight Generator
    - Report Writer
    """)

# ============================================================================
# LOAD DATA
# ============================================================================
@st.cache_data
def load_data():
    """Load sales data from CSV."""
    try:
        df = pd.read_csv("sales.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

# ============================================================================
# DASHBOARD MODE
# ============================================================================
if mode == "📊 Dashboard":
    st.markdown("<div class='main-header'><h1>📊 Sales Data Dashboard</h1></div>", unsafe_allow_html=True)
    
    if df is not None:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 Total Orders", len(df))
        with col2:
            st.metric("💰 Total Sales", f"${df['Sales'].sum():,.0f}")
        with col3:
            st.metric("🛍️ Units Sold", df['Quantity'].sum())
        with col4:
            st.metric("🏢 Regions", df['Region'].nunique())
        
        st.markdown("---")
        
        # Data table
        st.subheader("📋 Full Dataset")
        st.dataframe(df, width='stretch', height=400)
        
        # Quick breakdowns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sales by Product")
            product_sales = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)
            st.bar_chart(product_sales)
        
        with col2:
            st.subheader("Sales by Region")
            region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
            st.bar_chart(region_sales)
        
        st.markdown("---")
        st.subheader("Top Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            top_product = product_sales.idxmax()
            top_product_value = product_sales.max()
            st.markdown(f"""
            <div class='metric-card'>
            <strong>🏆 Top Product:</strong> {top_product}<br>
            <strong>Sales:</strong> ${top_product_value:,.0f}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            top_region = region_sales.idxmax()
            top_region_value = region_sales.max()
            st.markdown(f"""
            <div class='metric-card'>
            <strong>🌟 Top Region:</strong> {top_region}<br>
            <strong>Sales:</strong> ${top_region_value:,.0f}
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# ASK AI MODE
# ============================================================================
elif mode == "🔍 Ask AI":
    st.markdown("<div class='main-header'><h1>🔍 Ask Your AI Data Team</h1></div>", unsafe_allow_html=True)
    
    if st.session_state.demo_mode:
        st.markdown("""
        ### 🎬 Demo Mode - Sample Questions
        
        This dashboard is in **demo mode** showing pre-computed analysis results.  
        Click on a sample question to see results, then export to PDF/JSON.
        """)
        
        selected_question = st.selectbox(
            "📝 Select a sample question:",
            options=list(DEMO_ANALYSIS.keys())
        )
        
        if selected_question:
            st.markdown("---")
            st.subheader("📊 Analysis Result")
            st.write(DEMO_ANALYSIS[selected_question])
            
            st.success("✅ Demo analysis complete!")
            
            # Store in session state
            st.session_state.analysis_results = {
                'analyst_output': DEMO_ANALYSIS[selected_question],
                'report_output': DEMO_ANALYSIS[selected_question],
                'content': DEMO_ANALYSIS[selected_question],
                'question': selected_question
            }
    else:
        st.markdown("""
        Ask any question about your sales data. The AI team will analyze it and provide insights!
        
        **Example questions:**
        - Which region sold the most units?
        - What's the average sale price?
        - Compare sales between products
        - Give me insights on regional performance
        """)
        
        # User input
        user_question = st.text_area(
            "📝 Your Question:",
            placeholder="E.g., Which product had the highest sales?",
            height=100
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            analyze_button = st.button("🚀 Analyze", width='stretch', type="primary")
        
        if analyze_button and user_question:
            st.markdown("---")
            
            with st.spinner("🤖 AI Data Team is working on your question..."):
                try:
                    # Plan tasks
                    steps = plan_tasks(user_question)
                    
                    st.info(f"📋 **Execution Plan:** {' → '.join([s.upper() for s in steps])}")
                    
                    analyst_output = None
                    insights = None
                    report_output = None
                    
                    # Execute steps
                    for step in steps:
                        if step == "analyst":
                            with st.spinner("🔍 Data Analyst is analyzing..."):
                                analyst_output = analyze_data(user_question)
                            
                            st.subheader("📊 Data Analysis")
                            st.write(analyst_output)
                        
                        elif step == "insight":
                            if analyst_output:
                                with st.spinner("💡 Insight Generator is processing..."):
                                    insights = generate_insights(analyst_output)
                                
                                st.subheader("💡 Insights")
                                st.write(insights)
                        
                        elif step == "report":
                            if analyst_output:
                                with st.spinner("📄 Report Writer is drafting..."):
                                    report_output = generate_report(user_question, analyst_output, insights)
                                
                                st.subheader("📄 Report")
                                st.write(report_output)
                    
                    st.success("✅ Analysis complete!")
                    st.write(f"**Analyst output ready:** {len(analyst_output) if analyst_output else 0} chars")
                    st.write(f"**Report output ready:** {len(report_output) if report_output else 0} chars")
                    
                    # Store in session state so export buttons persist across reruns
                    st.session_state.analysis_results = {
                        'analyst_output': analyst_output,
                        'report_output': report_output,
                        'content': report_output or analyst_output,
                        'question': user_question
                    }
                
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                    logger.error(f"Analysis error: {e}")
        
        elif analyze_button:
            st.warning("⚠️ Please enter a question first!")
    
    # Show export buttons if we have results (they persist across reruns!)
    if st.session_state.analysis_results is not None:
        st.markdown("---")
        st.subheader("📥 Export Report")
        
        content = st.session_state.analysis_results['content']
        st.write(f"**Content to export:** {len(content)} characters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Export as JSON", width='stretch', key="ask_json"):
                st.info("Processing JSON export...")
                try:
                    logger.info(f"Exporting JSON, content length: {len(content)}")
                    result = export_report(content, format="json")
                    logger.info(f"JSON export result: {result}")
                    filename = Path(result['file_path']).name
                    st.success(f"✅ JSON exported: {filename}")
                except Exception as e:
                    logger.error(f"JSON Export error: {str(e)}", exc_info=True)
                    st.error(f"Export failed: {str(e)}")
        
        with col2:
            if st.button("📄 Export as PDF", width='stretch', key="ask_pdf"):
                st.info("Processing PDF export...")
                try:
                    question_title = st.session_state.analysis_results.get('question', 'Analysis Report')
                    logger.info(f"Exporting PDF with title: {question_title}")
                    result = export_report(
                        content,
                        format="pdf",
                        title=question_title
                    )
                    logger.info(f"PDF export result: {result}")
                    filename = Path(result['file_path']).name
                    st.success(f"✅ PDF exported: {filename}")
                except Exception as e:
                    logger.error(f"PDF Export error: {str(e)}", exc_info=True)
                    st.error(f"Export failed: {str(e)}")

# ============================================================================
# COMPARISONS MODE
# ============================================================================
elif mode == "📈 Comparisons":
    st.markdown("<div class='main-header'><h1>📈 Compare Your Data</h1></div>", unsafe_allow_html=True)
    
    if st.session_state.demo_mode:
        st.info("🎬 Demo mode - showing sample comparison data")
        
        comparison_type = st.radio(
            "What would you like to compare?",
            ["📍 Regional Performance", "🛍️ Product Comparison"],
            horizontal=True
        )
        
        if comparison_type == "📍 Regional Performance":
            result = """**Regional Performance Comparison**

Region A:
- Total Sales: $45,000 (35% of revenue)
- Units Sold: 1,250
- Avg Transaction: $1,200
- Orders: 38

Region B:
- Total Sales: $38,500 (30% of revenue)
- Units Sold: 980
- Avg Transaction: $1,100
- Orders: 35

Region C:
- Total Sales: $28,000 (22% of revenue)
- Units Sold: 750
- Avg Transaction: $950
- Orders: 29

Analysis: Region A leads in both volume and value, with 35% higher average transaction value than Region C."""
        else:
            result = """**Product Comparison Analysis**

Premium Widget:
- Revenue: $52,000 (35%)
- Units: 40
- Avg Price: $1,300
- Growth: +15% MoM

Standard Device:
- Revenue: $42,000 (28%)
- Units: 40
- Avg Price: $1,050
- Growth: +8% MoM

Basic Tool:
- Revenue: $35,000 (23%)
- Units: 40
- Avg Price: $875
- Growth: +5% MoM

Analysis: Premium Widget is the revenue leader and shows strongest growth momentum."""
        
        st.subheader(comparison_type)
        st.write(result)
        st.success("✅ Demo comparison loaded!")
        
        if st.button("💾 Export Comparison", type="primary", width='stretch'):
            try:
                export_result = export_report(
                    result,
                    format="json",
                    title=comparison_type
                )
                filename = Path(export_result['file_path']).name
                st.success(f"✅ Comparison exported: {filename}")
                st.balloons()
            except Exception as e:
                st.error(f"Export failed: {str(e)}")
    
    else:
        comparison_type = st.radio(
            "What would you like to compare?",
            ["📍 Regional Performance", "🛍️ Product Comparison"],
            horizontal=True
        )
        
        if st.button("🔄 Generate Comparison", type="primary", width='stretch'):
            with st.spinner("🤖 Comparing data..."):
                try:
                    if comparison_type == "📍 Regional Performance":
                        result = compare_regions()
                    else:
                        result = compare_products()
                    
                    st.subheader(comparison_type)
                    st.write(result)
                    
                    st.success("✅ Comparison complete!")
                    
                    if st.button("💾 Export Comparison"):
                        st.write("🔄 Exporting... (1/3)")
                        logger.info("Comparison Export started")
                        try:
                            st.write("🔄 Calling export function... (2/3)")
                            export_result = export_report(
                                result,
                                format="json",
                                title=comparison_type
                            )
                            st.write("🔄 Export complete! (3/3)")
                            logger.info(f"Export result: {export_result}")
                            
                            filename = Path(export_result['file_path']).name
                            logger.info(f"Comparison Export successful: {filename}")
                            st.success(f"✅ Comparison exported: {filename}")
                            st.balloons()
                        except Exception as e:
                            logger.error(f"Comparison Export error: {str(e)}", exc_info=True)
                            st.error(f"Export failed: {str(e)}")
                            st.write("Error details logged above ☝️")
                
                except Exception as e:
                    st.error(f"❌ Comparison failed: {str(e)}")
                    logger.error(f"Comparison error: {e}")

# ============================================================================
# REPORTS MODE
# ============================================================================
elif mode == "📄 Reports":
    st.markdown("<div class='main-header'><h1>📄 Generated Reports</h1></div>", unsafe_allow_html=True)
    
    exports_dir = Path("exports")
    
    if exports_dir.exists() and list(exports_dir.glob("*")):
        st.subheader("📋 Available Reports")
        
        # List reports
        reports = sorted(exports_dir.glob("*"), key=lambda x: x.stat().st_mtime, reverse=True)
        
        for report in reports[:10]:  # Show last 10
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"📄 {report.name}")
            
            with col2:
                file_size = report.stat().st_size / 1024  # KB
                st.caption(f"{file_size:.1f} KB")
            
            with col3:
                if report.suffix == ".json":
                    try:
                        with open(report) as f:
                            data = json.load(f)
                        st.download_button(
                            "⬇️ Download",
                            data=json.dumps(data, indent=2),
                            file_name=report.name
                        )
                    except Exception as e:
                        st.error(f"Error reading report: {e}")
                else:
                    with open(report, "rb") as f:
                        st.download_button(
                            "⬇️ Download",
                            data=f.read(),
                            file_name=report.name
                        )
        
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ Clear Old Reports", type="secondary", width='stretch'):
                try:
                    deleted_count = 0
                    for report in reports[10:]:
                        try:
                            report.unlink()
                            deleted_count += 1
                        except Exception as e:
                            st.warning(f"Could not delete {report.name}: {e}")
                    if deleted_count > 0:
                        st.success(f"✅ Cleared {deleted_count} old reports")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.info("No old reports to clear")
                except Exception as e:
                    st.error(f"Error clearing reports: {e}")
    else:
        st.info("📭 No reports generated yet. Use 'Ask AI' mode to create reports!")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px;'>
    🤖 AI Data Team • Powered by Multi-Agent LLM System  
    </div>
""", unsafe_allow_html=True)
