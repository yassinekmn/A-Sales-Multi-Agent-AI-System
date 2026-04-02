# main.py
"""Main entry point for the multi-agent AI system."""

from data_analyst_agent import analyze_data
from insight_generator_agent import generate_insights
from report_writer_agent import generate_report
from planner_agent import plan_tasks
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
                        report = generate_report(user_input, analyst_output, insights)
                        print("\n--- 📄 FINAL REPORT ---")
                        print(report)

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