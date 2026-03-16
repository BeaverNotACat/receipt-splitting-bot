import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from langchain.agents import create_agent, AgentState
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver  
from dataclasses import dataclass

from src.domain.models import Receipt
from src.domain.models.user import User
from src.domain.value_objects import LineItem
from src.application.common.agent import AgentI, Response

@dataclass
class UpdatedState(AgentState):
    receipt: Receipt
    users: list[User]

system_prompt='''You are Rozhkov'''

@tool
def assign_item(runtime: ToolRuntime[UpdatedState], item: LineItem, user: User)->Command:
    receipt = runtime.state.receipt
    try:
        receipt = receipt.assign_item(item, user)
        return Command(update={
            "receipt": receipt,
            "messages": [
                ToolMessage(
                    "Successfully updated receipt",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        })
    except Exception as e:
        return Command(update={
            "receipt": receipt,
            "messages": [
                ToolMessage(
                    f"Failed to update receipt: {str(e)}",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        })
    
@tool
def unassign_item(runtime: ToolRuntime[UpdatedState], item: LineItem, user: User)->Command:
    receipt = runtime.state.receipt
    try:
        receipt = receipt.disassign_item(item, user)
        return Command(update={
            "receipt": receipt,
            "messages": [
                ToolMessage(
                    "Successfully updated receipt",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        })
    except Exception as e:
        return Command(update={
            "receipt": receipt,
            "messages": [
                ToolMessage(
                    f"Failed to update receipt: {str(e)}",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        })

@tool
def append_unassigned(runtime: ToolRuntime[UpdatedState], item: LineItem)->Command:
    receipt = runtime.state.receipt
    try:
        receipt = receipt.append_item(item)
        return Command(update={
            "receipt": receipt,
            "messages": [
                ToolMessage(
                    "Successfully updated receipt",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        })
    except Exception as e:
        return Command(update={
            "receipt": receipt,
            "messages": [
                ToolMessage(
                    f"Failed to update receipt: {str(e)}",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        })

@tool
def remove_unassigned(runtime: ToolRuntime[UpdatedState], item: LineItem)->Command:
    receipt = runtime.state.receipt
    try:
        receipt = receipt.remove_item(item)
        return Command(update={
            "receipt": receipt,
            "messages": [
                ToolMessage(
                    "Successfully updated receipt",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        })
    except Exception as e:
        return Command(update={
            "receipt": receipt,
            "messages": [
                ToolMessage(
                    f"Failed to update receipt: {str(e)}",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        })


class Agent(AgentI):
    def __init__(self):
        model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        )
        self.agent = create_agent(model,
            tools=[assign_item, unassign_item, append_unassigned, remove_unassigned],
            system_prompt=system_prompt,
            state_schema=UpdatedState,
            checkpointer=InMemorySaver())        

    def invoke(self, user_prompt: str, receipt: Receipt, users: list[User])->Response:
        answ = self.agent.invoke({"messages": [{"role": "user", "content": user_prompt}]},
                            {"configurable": {"thread_id": receipt.id}},
                            context=UpdatedState(receipt=receipt, users = users),
                            )
        return answ
