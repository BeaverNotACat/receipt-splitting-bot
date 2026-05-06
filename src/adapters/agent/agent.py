from typing import TYPE_CHECKING, NewType

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.base import BaseCheckpointSaver

from src.adapters.agent.tools import (
    append_item,
    assign_item,
    remove_item,
    show_receipt,
    unassign_item,
)
from src.application.common.agent import AgentI, AgentResponse, HumanRequest
from src.application.common.locks import ReceiptLockI
from src.domain.services import ReceiptService, UserService
from src.domain.value_objects import AgentMessage

from .context import ReceiptModificationContext
from .state import InvokeState, ReceiptModificationState
from .templating import system_prompt_template, user_prompt_template

if TYPE_CHECKING:
    from typing import Any

    from src.domain.models import Receipt, User


AgentModelClient = NewType("AgentModelClient", ChatOpenRouter)


class Agent(AgentI):
    def __init__(
        self,
        client: AgentModelClient,
        checkpointer: BaseCheckpointSaver[str],
        receipt_lock: ReceiptLockI,
        user_service: UserService,
        receipt_service: ReceiptService,
    ) -> None:
        self.receipt_lock = receipt_lock
        self.user_service = user_service
        self.receipt_service = receipt_service
        self.agent = create_agent(
            client,
            tools=[
                append_item,
                assign_item,
                remove_item,
                show_receipt,
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
        async with self.receipt_lock(receipt.id):
            answer = await self.call_langchain(
                request, receipt, participants, []
            )

        return AgentResponse(
            answer=AgentMessage(answer["messages"][-1].content),
            updated_receipt=answer["receipt"],
        )

    async def call_langchain(
        self,
        request: HumanRequest,
        receipt: Receipt,
        participants: list[User],
        callbacks: list[BaseCallbackHandler],
    ) -> dict[str, Any]:
        """
        Method wraps bare langchain result for benching purposes
        """
        return await self.agent.ainvoke(
            input=self._construct_invoke_state(request, receipt, participants),
            config={
                "configurable": {"thread_id": str(receipt.id)},
                "max_concurrency": 1,
                "callbacks": callbacks,
            },
            context=self._construct_invoke_context(participants),
        )

    @staticmethod
    def _construct_invoke_state(
        request: HumanRequest, receipt: Receipt, participants: list[User]
    ) -> InvokeState:
        return {
            "messages": [
                HumanMessage(
                    user_prompt_template.render(
                        user_id=request.user_id,
                        user_input=request.users_input,
                        transcribed_photos=request.transcribed_photos,
                        transcribed_audios=request.transcribed_audios,
                    )
                ),
            ],
            "current_user_id": request.user_id,
            "receipt": receipt,
            "users": participants,
        }

    @staticmethod
    def _construct_invoke_context(
        participants: list[User],
    ) -> ReceiptModificationContext:
        return {"user_id_mapping": {user.id: user for user in participants}}
