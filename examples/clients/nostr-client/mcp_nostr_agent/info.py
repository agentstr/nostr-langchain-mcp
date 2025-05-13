from pydantic import BaseModel


class Skill(BaseModel):
    """Skill to be used by the agent."""

    name: str
    description: str


class AgentInfo(BaseModel):
    """Agent information."""

    name: str
    description: str
    skills: list[Skill]
    satoshis: int
    nostr_pubkey: str
