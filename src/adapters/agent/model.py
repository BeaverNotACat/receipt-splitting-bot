from langchain.agents import AgentState, create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

from src.adapters.agent.tools import (
    append_item,
    assign_item,
    remove_item,
    unassign_item,
)
from src.application.common.agent import AgentI, Response
from src.domain.models import Receipt
from src.domain.models.user import User


class UpdatedState(AgentState):
    receipt: Receipt
    users: list[User]


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
