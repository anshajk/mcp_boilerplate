# adk-agent

A minimal [Google ADK](https://google.github.io/adk-docs/) agent that connects
to the local `basic_server` MCP server (in [basic_server/server.py](../basic_server/server.py))
over stdio and exposes its `add`, `multiply`, and `compound_interest` tools.

## Setup

From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install google-adk litellm fastmcp
```

Set an OpenAI API key:

```bash
export OPENAI_API_KEY=your_key_here
```

## Run

Interactive CLI:

```bash
adk run adk-agent
```

Web UI:

```bash
adk web .
```

Try prompts like:

- "What's 23 + 19?"
- "Multiply 12 by 7."
- "If I invest $1000 at 5% compounded monthly for 10 years, what do I get?"
