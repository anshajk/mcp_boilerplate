# sqlite_mcp

A small [FastMCP](https://github.com/jlowin/fastmcp) server that exposes a local
SQLite database as MCP tools.

## Schema (sample data)

- **customers** (`id`, `name`, `email`, `city`, `signup_date`)
- **products** (`id`, `name`, `category`, `price`, `stock`)
- **orders** (`id`, `customer_id`, `product_id`, `quantity`, `total`, `order_date`)

## Tools

- `list_tables()` — list user tables
- `describe_table(table)` — column metadata
- `query(sql, limit=100)` — run a `SELECT` / `WITH` and return rows as dicts
- `execute(sql)` — run a non-`SELECT` statement (returns `rowcount`, `lastrowid`)

## Setup

From repo root:

```bash
pip install -r sqlite_mcp/requirements.txt
python sqlite_mcp/setup_db.py --reset
```

This creates `sqlite_mcp/store.db` populated with 25 customers, 12 products,
and 80 orders. Override the location with `--db /path/to/file.db` (and set
`SQLITE_MCP_DB` to the same path when running the server).

## Run standalone

```bash
python sqlite_mcp/server.py
```

The ADK agent in [adk_agent/agent.py](../adk_agent/agent.py) launches this
server automatically over stdio.
