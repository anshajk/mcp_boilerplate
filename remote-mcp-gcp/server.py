import asyncio
import logging
import os

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("MCP Server on Cloud Run")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Use this to add two numbers together.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of the two numbers.
    """
    logger.info(f">>> Tool: 'add' called with numbers '{a}' and '{b}'")
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Use this to subtract two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The difference of the two numbers.
    """
    logger.info(f">>> Tool: 'subtract' called with numbers '{a}' and '{b}'")
    return a - b


@mcp.tool()
def compound_interest(
    principal: float, annual_rate: float, times_per_year: int, years: float
) -> dict:
    """Calculate compound interest using the formula A = P * (1 + r/n)^(n*t).

    Args:
        principal (float): Initial amount of money.
        annual_rate (float): Annual interest rate as a decimal (e.g., 0.05 for 5%).
        times_per_year (int): Number of compounding periods per year (e.g., 12 for monthly).
        years (float): Number of years the money is invested or borrowed for.

    Returns:
        dict: A dictionary containing:
            - 'final_amount' (float): The total amount after interest.
            - 'interest_earned' (float): The interest earned (final_amount - principal).

    Raises:
        ValueError: If times_per_year is less than or equal to 0.
    """

    if times_per_year <= 0:
        raise ValueError("times_per_year must be > 0")
    amount = principal * (1 + annual_rate / times_per_year) ** (times_per_year * years)
    return {"final_amount": amount, "interest_earned": amount - principal}


if __name__ == "__main__":
    logger.info(f" MCP server started on port {os.getenv('PORT', 8080)}")
    # Could also use 'sse' transport, host="0.0.0.0" required for Cloud Run.
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8080),
        )
    )
