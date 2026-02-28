import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import dotenv

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


async def main():
    server_params = StdioServerParameters(
        command="npx",
        args=["mcp-remote", "https://mcp.kite.trade/mcp"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)

            llm = ChatOpenAI(model="gpt-4o")
            memory = MemorySaver()
            agent = create_react_agent(llm, tools, checkpointer=memory)

            config = {"configurable": {"thread_id": "chat_session"}}
            print("Agent ready. Type 'quit' or 'exit' to end the chat.")

            loop = asyncio.get_running_loop()
            while True:
                print("\nYou: ", end="")
                sys.stdout.flush()
                user_msg = await loop.run_in_executor(None, sys.stdin.readline)
                user_msg = user_msg.strip()

                if user_msg.lower() in ["quit", "exit", "q"]:
                    break

                if not user_msg:
                    continue

                response = await agent.ainvoke(
                    {"messages": [("user", user_msg)]}, config=config
                )

                messages = response.get("messages", [])
                if messages:
                    print(f"Agent: {messages[-1].content}")


if __name__ == "__main__":
    asyncio.run(main())
