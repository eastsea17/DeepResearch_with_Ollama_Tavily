import json
import re
from llm_client import OllamaClient
from tavily_client import TavilyClient

class DeepResearchAgent:
    def __init__(self):
        self.llm = OllamaClient()
        self.tavily = TavilyClient()

    def run(self, user_query, search_depth=None):
        """
        Executes the deep research process.
        """
        print(f"--- Starting Research on: {user_query} ---")
        
        # Step 1: Plan and Generate Search Queries
        search_queries = self._plan_research(user_query)
        if not search_queries:
            return {
                "query": user_query,
                "search_results": [],
                "final_answer": "Failed to generate search queries."
            }

        # Step 2: Execute Search
        print(f"--- Executing {len(search_queries)} Search Queries ---")
        search_results = []
        for query in search_queries:
            print(f"Searching for: {query}")
            # Pass search_depth if provided, otherwise TavilyClient uses default from config
            kwargs = {}
            if search_depth:
                kwargs["search_depth"] = search_depth
            
            result = self.tavily.search(query, **kwargs)
            search_results.append(result)

        # Step 3: Synthesize Results
        print("--- Synthesizing Results ---")
        final_answer = self._synthesize_answer(user_query, search_results)
        
        return {
            "query": user_query,
            "search_results": search_results,
            "final_answer": final_answer
        }

    def _plan_research(self, query):
        """
        Asks the LLM to plan the research and generate search queries.
        """
        system_prompt = (
            "You are a Deep Research Agent powered by DeepSeek-R1. "
            "Your goal is to create a comprehensive research plan for a given user query. "
            "You MUST first think about the problem in a <think> block, analyzing what information is missing and what needs to be searched. "
            "After thinking, you MUST output a list of search queries in a strict JSON format. "
            "The JSON should be a list of strings, e.g., [\"query 1\", \"query 2\"]. "
            "Do not output any text outside of the <think> block and the JSON block."
        )
        
        user_prompt = f"User Query: {query}\n\nGenerate the research plan and search queries."
        
        response = self.llm.generate(user_prompt, system_prompt=system_prompt)
        
        # Extract thinking process for display (optional)
        think_match = re.search(r"<think>(.*?)</think>", response, re.DOTALL)
        if think_match:
            print("\n[Agent Thinking Process]:")
            print(think_match.group(1).strip())
            print("-" * 30)
        
        # Extract JSON
        # Try to find JSON array in the response
        json_match = re.search(r"\[.*\]", response, re.DOTALL)
        if json_match:
            try:
                queries = json.loads(json_match.group(0))
                return queries
            except json.JSONDecodeError:
                print("Error decoding JSON from LLM response.")
                print(f"Raw response: {response}")
                return []
        else:
            print("No JSON found in LLM response.")
            print(f"Raw response: {response}")
            return []

    def _synthesize_answer(self, query, search_results):
        """
        Synthesizes the final answer from search results.
        """
        # Format search results for the LLM
        context = ""
        for i, res in enumerate(search_results):
            context += f"Source {i+1}:\n"
            if "results" in res:
                for item in res["results"]:
                    context += f"- Title: {item.get('title')}\n"
                    context += f"  Content: {item.get('content')}\n"
                    context += f"  URL: {item.get('url')}\n"
            context += "\n"

        system_prompt = (
            "You are a Deep Research Agent. "
            "You have performed a search to answer the user's query. "
            "Synthesize the information from the provided search results into a comprehensive, well-structured answer. "
            "Use the <think> block to structure your response and verify the information before writing the final answer. "
            "Cite your sources where appropriate."
        )
        
        user_prompt = (
            f"User Query: {query}\n\n"
            f"Search Results:\n{context}\n\n"
            "Provide the final answer."
        )
        
        response = self.llm.generate(user_prompt, system_prompt=system_prompt)
        return response

if __name__ == "__main__":
    # Test run (requires valid API key in .env)
    agent = DeepResearchAgent()
    # print(agent.run("What is the latest version of Python?"))
