"""SQLite MCP server.

Exposes read-only-ish tools over a local SQLite database:
  - list_tables: list all user tables
  - describe_table: show columns and types for a table
  - query: run a single SELECT statement and return rows
  - execute: run a single non-SELECT statement (INSERT/UPDATE/DELETE)

The database path defaults to ``store.db`` in this directory and can be
overridden via the ``SQLITE_MCP_DB`` environment variable.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from fastmcp import FastMCP

DEFAULT_DB_PATH = Path(__file__).parent / "store.db"
DB_PATH = Path(os.environ.get("SQLITE_MCP_DB", DEFAULT_DB_PATH))

mcp = FastMCP("SQLite MCP server")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@mcp.tool()
def list_tables() -> list[str]:
    """List all user-defined tables in the database."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
    return [r["name"] for r in rows]


@mcp.tool()
def describe_table(table: str) -> list[dict]:
    """Return column metadata for a table.

    Args:
        table: Table name.

    Returns:
        List of dicts with keys: name, type, notnull, default, pk.
    """
    with _connect() as conn:
        rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return [
        {
            "name": r["name"],
            "type": r["type"],
            "notnull": bool(r["notnull"]),
            "default": r["dflt_value"],
            "pk": bool(r["pk"]),
        }
        for r in rows
    ]


@mcp.tool()
def query(sql: str, limit: int = 100) -> list[dict]:
    """Run a single SELECT statement and return up to ``limit`` rows.

    Args:
        sql: A SELECT statement. Other statement types are rejected.
        limit: Maximum number of rows to return (default 100).
    """
    stripped = sql.strip().rstrip(";").strip()
    if not stripped.lower().startswith(("select", "with")):
        raise ValueError("Only SELECT/WITH statements are allowed in query().")
    with _connect() as conn:
        cur = conn.execute(stripped)
        rows = cur.fetchmany(limit)
    return [dict(r) for r in rows]


@mcp.tool()
def execute(sql: str) -> dict:
    """Run a single non-SELECT statement (INSERT/UPDATE/DELETE).

    Returns a dict with ``rowcount`` and ``lastrowid``.
    """
    stripped = sql.strip().rstrip(";").strip()
    lowered = stripped.lower()
    if lowered.startswith(("select", "with")):
        raise ValueError("Use query() for SELECT statements.")
    with _connect() as conn:
        cur = conn.execute(stripped)
        conn.commit()
        return {"rowcount": cur.rowcount, "lastrowid": cur.lastrowid}


if __name__ == "__main__":
    mcp.run()
