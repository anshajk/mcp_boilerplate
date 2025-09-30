from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from app import app

mcp = FastMCP.from_fastapi(app, name="E-Commerce MCP Server")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    return JSONResponse({"status": "healthy"})


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="localhost", port=8020)
