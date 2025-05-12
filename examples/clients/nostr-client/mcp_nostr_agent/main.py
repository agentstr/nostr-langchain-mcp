from fastapi import FastAPI, Depends
from langgraph.graph.graph import CompiledGraph

from mcp_nostr_agent.agent import mcp_client
from pydantic import BaseModel


class ChatInput(BaseModel):
    messages: list[str]
    thread_id: str


app = FastAPI()


@app.post("/chat")
async def chat(input: ChatInput):
    config = {"configurable": {"thread_id": input.thread_id}}
    async with mcp_client() as graph:
        response = await graph.ainvoke({"messages": input.messages}, config=config)
    return response["messages"][-1].content
