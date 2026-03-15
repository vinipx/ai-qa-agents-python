from typing import Annotated, TypedDict, List
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Represents the state of our multi-agent framework.
    """
    messages: Annotated[List[BaseMessage], operator.add]
    plan: str
    approved: bool
    metrics: dict  # To store lead time, tokens, cost
    next_agent: str
    sender: str # Track who sent the message to the supervisor
