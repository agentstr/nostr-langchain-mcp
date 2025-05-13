from fastapi import FastAPI
from mcp_nostr_agent.agent import mcp_client, get_tools
from mcp_nostr_agent.info import AgentInfo, Skill
from pydantic import BaseModel


class ChatInput(BaseModel):
    messages: list[str]
    thread_id: str


app = FastAPI()


@app.get("/info")
async def info():
    skills = []
    async def get_skills():
        async with get_tools() as tools:
            for tool in tools:
                skills.append(
                    Skill(
                        name=tool.name,
                        description=tool.description,
                    )
                )
    await get_skills()
    return AgentInfo(
        name='Simple Nostr Agent',
        description='Helps perform a variety of simple tasks in Python.',
        skills=skills,
        satoshis=50,
        nostr_pubkey='your_nostr_pubkey_here',
    ).model_dump()


@app.post("/chat")
async def chat(input: ChatInput):
    config = {"configurable": {"thread_id": input.thread_id}}
    async with mcp_client() as graph:
        response = await graph.ainvoke({"messages": input.messages}, config=config)
    return response["messages"][-1].content
