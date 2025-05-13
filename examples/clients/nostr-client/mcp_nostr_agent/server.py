import os
from fastapi import FastAPI
from mcp_nostr_agent.agent import mcp_client, get_tools
from mcp_nostr_agent.info import AgentInfo, Skill
from pynostr.key import PrivateKey
from pydantic import BaseModel


class ChatInput(BaseModel):
    messages: list[str]
    thread_id: str


app = FastAPI()


@app.get("/info")
async def info():
    async def get_skills():
        async with get_tools() as tools:
            return [Skill(
                    name=tool.name,
                    description=tool.description,
                ) for tool in tools]
    skills = await get_skills()
    return AgentInfo(
        name='Simple Nostr Agent',
        description='Helps perform a variety of simple tasks in Python.',
        skills=skills,
        satoshis=50,
        nostr_pubkey=PrivateKey.from_nsec(os.getenv('NOSTR_CLIENT_PRIVATE_KEY')).public_key.bech32(),
    ).model_dump()


@app.post("/chat")
async def chat(input: ChatInput):
    config = {"configurable": {"thread_id": input.thread_id}}
    async with mcp_client() as graph:
        response = await graph.ainvoke({"messages": input.messages}, config=config)
    return response["messages"][-1].content
