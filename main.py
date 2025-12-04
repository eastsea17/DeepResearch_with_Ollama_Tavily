import argparse
import os
import sys
from dotenv import load_dotenv
from agent import DeepResearchAgent

from report_generator import generate_html_report
from config import LLMConfig

def main():
    # Load environment variables
    load_dotenv()
    
    # Check for API Key
    if not os.getenv("TAVILY_API_KEY"):
        print("Error: TAVILY_API_KEY not found.")
        print("Please create a .env file with your TAVILY_API_KEY.")
        print("Example: TAVILY_API_KEY=tvly-...")
        sys.exit(1)

    # Parse Command Line Arguments
    parser = argparse.ArgumentParser(description="Deep Research Agent powered by DeepSeek-R1")
    parser.add_argument("query", nargs="?", help="The research topic")
    parser.add_argument("--advanced", action="store_true", help="Use advanced search depth")
    parser.add_argument("--model", choices=["local", "deepseek-cloud", "gpt-cloud"], default=None, help="Select the LLM model to use")
    args = parser.parse_args()

    # Map model choice to config constant
    model_map = {
        "local": LLMConfig.MODEL_LOCAL,
        "deepseek-cloud": LLMConfig.MODEL_DEEPSEEK_CLOUD,
        "gpt-cloud": LLMConfig.MODEL_GPT_OSS_CLOUD
    }
    
    if args.model:
        selected_model = model_map[args.model]
    else:
        selected_model = LLMConfig.MODEL_NAME

    search_depth = "advanced" if args.advanced else "basic"

    print("==========================================")
    print("      Deep Research Agent (DeepSeek-R1)   ")
    print("==========================================")
    print("      Deep Research Agent (DeepSeek-R1)   ")
    print(f"      Mode: {search_depth.upper()}        ")
    print(f"      Model: {selected_model}             ")
    print("==========================================")

    if args.query:
        # Single run mode
        run_research(args.query, search_depth, selected_model)
    else:
        # Interactive mode
        interactive_loop(search_depth, selected_model)

def run_research(query, search_depth, model_name):
    try:
        agent = DeepResearchAgent(model_name=model_name)
        result_data = agent.run(query, search_depth=search_depth)
        
        print("\n" + "="*40)
        print("FINAL ANSWER")
        print("="*40 + "\n")
        print(result_data["final_answer"])
        
        # Generate Report
        report_path = generate_html_report(result_data)
        print(f"\nReport generated: {report_path}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

def interactive_loop(default_search_depth, model_name):
    while True:
        try:
            user_query = input("\nEnter your research topic (or 'exit' to quit): ").strip()
            if user_query.lower() in ['exit', 'quit']:
                print("Exiting...")
                break
            
            if not user_query:
                continue

            run_research(user_query, default_search_depth, model_name)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
