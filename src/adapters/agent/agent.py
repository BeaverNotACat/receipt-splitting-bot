from typing import TYPE_CHECKING, NewType

from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.base import BaseCheckpointSaver

from src.adapters.agent.tools import (
    append_item,
    assign_item,
    remove_item,
    unassign_item,
)
from src.application.common.agent import AgentI, AgentResponse, HumanRequest
from src.domain.services import ReceiptService, UserService
from src.domain.value_objects import AgentMessage, UserID

from .context import ReceiptModificationContext
from .state import InvokeState, ReceiptModificationState
from .templating import system_prompt_template

if TYPE_CHECKING:
    from src.domain.models import Receipt, User


AgentModelClient = NewType("AgentModelClient", ChatOpenRouter)


class Agent(AgentI):
    def __init__(
        self,
        client: AgentModelClient,
        checkpointer: BaseCheckpointSaver[str],
        user_service: UserService,
        receipt_service: ReceiptService,
    ) -> None:
        self.user_service = user_service
        self.receipt_service = receipt_service
        self.agent = create_agent(
            client,
            tools=[
                append_item,
                assign_item,
                remove_item,
                unassign_item,
            ],
            system_prompt=system_prompt_template.render(),
            state_schema=ReceiptModificationState,
            context_schema=ReceiptModificationContext,
            checkpointer=checkpointer,
        )

    async def invoke(
        self, request: HumanRequest, receipt: Receipt, participants: list[User]
    ) -> AgentResponse:
        answer = await self.agent.ainvoke(
            input=self._construct_invoke_state(request, receipt, participants),
            config={"configurable": {"thread_id": receipt.id}},
            context=self._construct_invoke_context(participants),
        )

        return AgentResponse(
            answer=AgentMessage(answer["messages"][-1].content),
            updated_receipt=answer["receipt"],
        )

    def _construct_invoke_state(
        self, request: HumanRequest, receipt: Receipt, participants: list[User]
    ) -> InvokeState:
        return {
            "messages": [
                self._construct_receipt_state_message(
                    receipt, participants, request.user_id
                ),
                self._construct_human_message(request),
            ],
            "current_user_id": request.user_id,
            "receipt": receipt,
            "users": participants,
        }

    @staticmethod
    def _construct_receipt_state_message(
        receipt: Receipt, participants: list[User], current_user_id: UserID
    ) -> SystemMessage:
        # TODO(beavernotacat): Switch from receipt data spamming
        # https://github.com/BeaverNotACat/receipt-splitting-bot/issues/50
        message_text = (
            f"ID текущего пользователя: {current_user_id}"
            "Состояние чека:\n"
            f"{receipt!s}\n"
            "Список участников чека\n"
            f"{participants!s}"
        )
        return SystemMessage(message_text)

    @staticmethod
    def _construct_human_message(request: HumanRequest) -> HumanMessage:
        # TODO(beavernotacat): Enchance HumanMessage prompt
        # https://github.com/BeaverNotACat/receipt-splitting-bot/issues/45
        message_text = (
            (
                str(request.users_input)
                if request.users_input is not None
                else ""
            )
            + "\n".join(request.transcribed_photos)
            + "\n".join(request.transcribed_audios)
        )
        return HumanMessage(message_text)

    @staticmethod
    def _construct_invoke_context(
        participants: list[User],
    ) -> ReceiptModificationContext:
        return {"user_id_mapping": {user.id: user for user in participants}}
