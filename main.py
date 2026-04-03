# main.py
"""Main entry point for the multi-agent AI system."""

from data_analyst_agent import analyze_data
from insight_generator_agent import generate_insights
from report_writer_agent import generate_report
from planner_agent import plan_tasks
from export_agent import export_report
from comparison_agent import compare_regions, compare_products, compare_head_to_head
from utils.logger import get_logger
from utils.errors import AgentExecutionError, DataValidationError

logger = get_logger(__name__)


def main():
    """Run the AI Data Team interactive loop."""
    print("=" * 50)
    print("🤖 AI Data Team (Autonomous Multi-Agent System)")
    print("=" * 50)
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("\n📊 Ask your AI Data Team: ").strip()

            if not user_input:
                print("⚠️  Please enter a question.")
                continue

            if user_input.lower() == "exit":
                print("\n👋 Goodbye!")
                break

            # Get execution plan
            try:
                steps = plan_tasks(user_input)
                print(f"\n📋 Planner decided: {' → '.join(steps).upper()}\n")
            except Exception as e:
                logger.error(f"Planning failed: {e}")
                print("❌ Planning failed. Using default workflow.")
                steps = ["analyst", "insight", "report"]

            analyst_output = None
            insights = None
            report_output = None

            # Execute planned steps
            for step in steps:
                try:
                    if step == "analyst":
                        print("🔍 Data Analyst is analyzing...")
                        analyst_output = analyze_data(user_input)
                        print("\n--- 📊 DATA ANALYSIS ---")
                        print(analyst_output)

                    elif step == "insight":
                        if not analyst_output:
                            print("⚠️  Skipping insights (no analysis available)")
                            continue
                        
                        print("\n💡 Insight Generator is processing...")
                        insights = generate_insights(analyst_output)
                        print("\n--- 💡 INSIGHTS ---")
                        print(insights)

                    elif step == "report":
                        if not analyst_output:
                            print("⚠️  Skipping report (no analysis available)")
                            continue
                        
                        print("\n📄 Report Writer is drafting...")
                        report_output = generate_report(user_input, analyst_output, insights)
                        print("\n--- 📄 FINAL REPORT ---")
                        print(report_output)

                    elif step == "comparison":
                        print("\n📊 Comparison Agent is analyzing...")
                        # Determine comparison type from user input
                        if "region" in user_input.lower():
                            comparison = compare_regions()
                        elif "product" in user_input.lower():
                            comparison = compare_products()
                        else:
                            comparison = compare_regions()  # Default
                        print("\n--- 📊 COMPARISON ANALYSIS ---")
                        print(comparison)

                    elif step == "export":
                        if not report_output and not analyst_output:
                            print("⚠️  Skipping export (no analysis available)")
                            continue
                        
                        print("\n💾 Export Agent is preparing...")
                        content = report_output or analyst_output
                        
                        # Detect export format from user input
                        export_format = 'json'  # Default format
                        user_lower = user_input.lower()
                        if 'pdf' in user_lower:
                            export_format = 'pdf'
                        elif 'html' in user_lower:
                            export_format = 'html'
                        elif 'txt' in user_lower or 'text' in user_lower:
                            export_format = 'txt'
                        elif 'excel' in user_lower or 'xlsx' in user_lower:
                            export_format = 'json'  # Keep as JSON for now (Excel would need tabular data)
                        
                        export_result = export_report(content, format=export_format)
                        print("\n--- 💾 EXPORT RESULT ---")
                        print(f"✓ Report exported to: {export_result['file_path']}")
                        print(f"  Format: {export_result['format']}")
                        print(f"  Size: {export_result['size_bytes']} bytes")

                except DataValidationError as e:
                    logger.error(f"Data validation error in {step}: {e}")
                    print(f"❌ Data error: {e}")
                    break
                except AgentExecutionError as e:
                    logger.error(f"Agent execution error: {e}")
                    print(f"❌ Agent error: {e}")
                    if step == "analyst":
                        # Can't continue without analysis
                        break

            print("\n" + "=" * 50 + "\n")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            print(f"❌ Unexpected error: {e}")
            print("Please try again or type 'exit' to quit.\n")


if __name__ == "__main__":
    main()