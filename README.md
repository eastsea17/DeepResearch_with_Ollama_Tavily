# Deep Research Agent with Ollama & Tavily

A powerful, local Deep Research Agent that leverages **DeepSeek-R1** (via Ollama) for reasoning and **Tavily API** for real-time web search. This agent plans its research, executes search queries, and synthesizes comprehensive answers with citations.

## Features

- **Local LLM Intelligence**: Uses `deepseek-r1:8b` running locally on Ollama for privacy and cost-efficiency.
- **Real-time Web Search**: Integrates with Tavily API to fetch the latest information.
- **Smart Planning**: The agent "thinks" about the user's query to generate targeted search plans.
- **HTML Reporting**: Automatically generates detailed HTML reports with search results and final answers.
- **CLI & Interactive Modes**: Flexible usage options.

## Prerequisites

1.  **Python 3.8+**
2.  **Ollama**: Installed and running.
    - Pull the model: `ollama pull deepseek-r1:8b`
    - Start the server: `ollama serve`
3.  **Tavily API Key**: Get one at [tavily.com](https://tavily.com).

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  Install dependencies:
    ```bash
    pip install requests python-dotenv markdown
    ```

3.  Set up environment variables:
    - Create a `.env` file (or copy `.env.example`):
      ```bash
      cp .env.example .env
      ```
    - Edit `.env` and add your API key:
      ```env
      TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
      ```

## Usage

### Interactive Mode
Run the agent and enter queries interactively:
```bash
python main.py
```

### Command Line Mode
Run a single query directly from the terminal:
```bash
python main.py "What is the latest news on Solid State Batteries?" --advanced
```
- `--advanced`: (Optional) Use advanced search depth for more comprehensive results.

## Configuration

You can adjust settings in `config.py`:
- **TavilyConfig**: `SEARCH_DEPTH`, `MAX_RESULTS`, etc.
- **LLMConfig**: `MODEL_NAME`, `TEMPERATURE`, `CONTEXT_WINDOW`.
- **ReportConfig**: `RESULTS_DIR`.

## Output

- **Console**: Displays the agent's thinking process, search queries, and final answer.
- **HTML Reports**: Saved in the `results/` directory (e.g., `results/research_report_20251204_083047.html`).

## License

MIT License
