import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.


def _ensure_env(var: str):
    if not os.environ.get(var):
        raise RuntimeError(f"{var} is not set. Please set it in your environment or .env file.")


_ensure_env("ANTHROPIC_API_KEY")

model = ChatAnthropic(temperature=0, model_name="claude-3-7-sonnet-latest")
relays = os.getenv('NOSTR_RELAYS').split(',')
private_key = os.getenv('NOSTR_CLIENT_PRIVATE_KEY')
server_public_key = os.getenv('NOSTR_SERVER_PUBLIC_KEY')
nwc_str = os.getenv('NOSTR_NWC_STR')


async def mcp_client():
    async with MultiServerMCPClient(
        {
            "nostr": {
                "relays": relays,
                "server_public_key": server_public_key,
                "private_key": private_key,
                "nwc_str": "not yet implemented",
                "transport": "nostr",
            },
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        for output in agent.stream({"messages": "what's the weather in portland?"}, stream_mode="updates"):
            print(output)
        for output in agent.stream({"messages": "what's the current date and time?"}):
            print(output)


if __name__ == '__main__':
    import asyncio
    asyncio.run(mcp_client())

