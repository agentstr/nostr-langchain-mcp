import os
from contextlib import asynccontextmanager

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.


def _ensure_env(var: str):
    if not os.environ.get(var):
        raise RuntimeError(f"{var} is not set. Please set it in your environment or .env file.")


_ensure_env("ANTHROPIC_API_KEY")

model = ChatAnthropic(temperature=0, model_name="claude-3-7-sonnet-latest")


@asynccontextmanager
async def get_tools():
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('NOSTR_CLIENT_PRIVATE_KEY')
    server_public_key = os.getenv('NOSTR_SERVER_PUBLIC_KEY')
    nwc_str = os.getenv('NWC_CONN_STR')
    async with MultiServerMCPClient(
        {
            "nostr": {
                "relays": relays,
                "server_public_key": server_public_key,
                "private_key": private_key,
                "nwc_str": nwc_str,
                "transport": "nostr",
            },
        }
    ) as client:
        yield client.get_tools()


@asynccontextmanager
async def mcp_client():
    async with get_tools() as tools:
        agent = create_react_agent(model, tools, checkpointer=MemorySaver())
        yield agent


if __name__ == '__main__':
    import asyncio

    async def run():
        async with mcp_client() as agent:
            async for output in agent.astream({"messages": "what's the weather in portland?"}, stream_mode="updates"):
                print(output)
            async for output in agent.astream({"messages": "what's the current date and time?"}):
                print(output)

    asyncio.run(run())

