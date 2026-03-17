from langchain.agents import AgentState, create_agent
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from src.application.common.agent import AgentI, Response
from src.domain.exceptions import DomainError
from src.domain.models import Receipt
from src.domain.models.user import User
from src.domain.value_objects import LineItem


class UpdatedState(AgentState):
    receipt: Receipt
    users: list[User]


system_prompt = """You are Rozhkov"""


@tool
def assign_item(
    runtime: ToolRuntime,
    item: LineItem,
    user: User,
) -> Command:
    receipt = runtime.state["receipt"]
    try:
        receipt = receipt.assign_item(item, user)
        message = ToolMessage(
            "Successfully updated receipt",
            tool_call_id=runtime.tool_call_id,
        )
    except DomainError as err:
        message = ToolMessage(
            f"Failed to update receipt: {err!s}",
            tool_call_id=runtime.tool_call_id,
        )

    return Command(
        update={
            "receipt": receipt,
            "messages": [message],
        }
    )


@tool
def unassign_item(
    runtime: ToolRuntime[UpdatedState], item: LineItem, user: User
) -> Command:
    receipt = runtime.state["receipt"]
    try:
        receipt = receipt.disassign_item(item, user)
        message = ToolMessage(
            "Successfully updated receipt",
            tool_call_id=runtime.tool_call_id,
        )
    except DomainError as err:
        message = ToolMessage(
            f"Failed to update receipt: {err!s}",
            tool_call_id=runtime.tool_call_id,
        )

    return Command(
        update={
            "receipt": receipt,
            "messages": [message],
        }
    )


@tool
def append_unassigned(
    runtime: ToolRuntime[UpdatedState], item: LineItem
) -> Command:
    receipt = runtime.state["receipt"]
    try:
        receipt = receipt.append_item(item)
        message = ToolMessage(
            "Successfully updated receipt",
            tool_call_id=runtime.tool_call_id,
        )
    except DomainError:
        return Command(
            update={
                "receipt": receipt,
                "messages": [
                    ToolMessage(
                        f"Failed to update receipt: {e!s}",
                        tool_call_id=runtime.tool_call_id,
                    )
                ],
            }
        )


@tool
def remove_unassigned(
    runtime: ToolRuntime[UpdatedState], item: LineItem
) -> Command:
    receipt = runtime.state.receipt
    try:
        receipt = receipt.remove_item(item)
        return Command(
            update={
                "receipt": receipt,
                "messages": [
                    ToolMessage(
                        "Successfully updated receipt",
                        tool_call_id=runtime.tool_call_id,
                    )
                ],
            }
        )
    except Domainerror as e:
        return Command(
            update={
                "receipt": receipt,
                "messages": [
                    ToolMessage(
                        f"Failed to update receipt: {e!s}",
                        tool_call_id=runtime.tool_call_id,
                    )
                ],
            }
        )


class Agent(AgentI):
    def __init__(self) -> None:
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        self.agent = create_agent(
            model,
            tools=[
                assign_item,
                unassign_item,
                append_unassigned,
                remove_unassigned,
            ],
            system_prompt=system_prompt,
            state_schema=UpdatedState,
            checkpointer=InMemorySaver(),
        )

    def invoke(
        self, user_prompt: str, receipt: Receipt, users: list[User]
    ) -> Response:
        return self.agent.invoke(
            {"messages": [{"role": "user", "content": user_prompt}]},
            {"configurable": {"thread_id": receipt.id}},
            context=UpdatedState(receipt=receipt, users=users),
        )
