from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

from src.adapters.agent.tools import (
    append_item,
    assign_item,
    remove_item,
    unassign_item,
)
from src.adapters.agent.tools.base import ReceiptModificationState
from src.application.common.agent import AgentI, Response
from src.domain.models import ReceiptItemsData
from src.domain.models.user import User
from src.domain.value_objects import ReceiptID

system_prompt = """You are Rozhkov"""


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
                append_item,
                assign_item,
                remove_item,
                unassign_item,
            ],
            system_prompt=system_prompt,
            state_schema=ReceiptModificationState,
            checkpointer=InMemorySaver(),
        )

    def invoke(
        self, user_prompt: str, receipt_items_data: ReceiptItemsData,
        users: tuple[User, ...], tread_id: ReceiptID
    ) -> Response:
        return self.agent.invoke(
            {"messages": [{"role": "user", "content": user_prompt}],
             "receipt_items_data": receipt_items_data,
             "users": users},
            {"configurable": {"thread_id": tread_id}},
        )
