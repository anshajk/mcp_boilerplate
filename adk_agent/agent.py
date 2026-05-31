"""ADK agent wired to the local basic_server (math) and sqlite_mcp servers over stdio."""

import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp.client.stdio import StdioServerParameters

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_MATH_SERVER = os.path.join(_REPO_ROOT, "basic_server", "server.py")
_SQLITE_SERVER = os.path.join(_REPO_ROOT, "sqlite_mcp", "server.py")


def _stdio_toolset(script_path: str) -> MCPToolset:
    return MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="python",
                args=[script_path],
            ),
        ),
    )


root_agent = Agent(
    name="math_and_store_agent",
    model=LiteLlm(model="openai/gpt-4o"),
    instruction=(
        "You are a helpful assistant with two skill sets:\n"
        "1. Math: use the math tools (add, multiply, compound_interest) for any "
        "arithmetic. Always call a tool rather than computing in your head.\n"
        "2. Store database: use the sqlite tools (list_tables, describe_table, "
        "query, execute) to answer questions about the local store database "
        "(customers, products, orders). Prefer `query` with a SELECT statement "
        "and inspect the schema with `list_tables` / `describe_table` first if "
        "you are unsure of column names."
    ),
    tools=[
        _stdio_toolset(_MATH_SERVER),
        _stdio_toolset(_SQLITE_SERVER),
    ],
)
