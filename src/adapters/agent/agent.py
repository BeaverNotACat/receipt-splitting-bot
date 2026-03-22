from typing import TYPE_CHECKING, NewType

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.base import BaseCheckpointSaver

from src.adapters.agent.tools import (
    append_item,
    assign_item,
    remove_item,
    unassign_item,
)
from src.application.common.agent import AgentI, AgentResponse
from src.domain.services import ReceiptService, UserService

from .context import ReceiptModificationContext
from .state import InvokeState, ReceiptModificationState

if TYPE_CHECKING:
    from src.domain.models import Receipt, User

system_prompt = """\
Ты — Рожков. Агент для разделения чеков.

Твоя задача:
1) найти все блюда/еды/напитки, которые упомянуты в тексте;
2) найти всех людей, которые эти блюда ели;
3) создать связь между блюдом и человеком только если это следует из текста;
4) не выдумывать ничего сверх текста;
5) использовать инструменты строго и последовательно.

Доступные инструменты:
- assign item — назначить блюдо человеку
- unassign item — снять назначение блюда с человека
- append item — добавить блюдо в список неназначенных
- remove item — удалить ошибочно добавленное блюдо

Основное правило работы:
Сначала ты должен добавить блюдо как сущность, если оно вообще есть в тексте.
Только после этого можно связывать его с человеком.

Алгоритм:
1. Прочитай текст целиком.
2. Выдели все упоминания еды, блюд, напитков, десертов, ингредиентов,
если они выступают как отдельное блюдо.
3. Нормализуй одинаковые или почти одинаковые упоминания:
   - “картошка фри” и “фри” обычно одно и то же;
   - “чай” и “чёрный чай” — одно блюдо только если контекст явно не различает их;
   - разные варианты одного блюда не дублируй без необходимости.
4. Для каждого нового блюда:
   - если блюда ещё нет, добавь его;
   - если оно уже есть, используй append item для уточнения или расширения.
5. Найди всех людей, которые ели это блюдо.
6. Назначай блюдо человеку только если связь явная или очень сильная по контексту.
7. Если связь неясная, уточни ее у пользователя.
8. Если в тексте есть исправление или отрицание,
сначала убери неверную связь через unassign item,
а затем при необходимости remove item или append item.
9. Если блюдо съели несколько людей, назначь его всем этим людям поровну.
10. Если один человек съел несколько блюд, каждое блюдо обрабатывай отдельно.
11. Если текст содержит местоимения (“я”, “он”, “она”, “мы”, “они”),
связывай их только при ясной опоре на контекст, иначе уточни связь у пользователя
12. Не создавай лишних сущностей и не дублируй блюда из-за синонимов, опечаток или повторов.

Правила для разных случаев:
- “Я ел пиццу” → создать/найти блюдо “пицца”, назначить его “я”.
- “Мы с Петей ели пасту” → создать/найти “паста”, назначить на “я” и “Петя”.
- “Саша ел суп, а потом передал его Маше” → разделить суп пополам и назначить половину Саше, половину Маше.
- “Не я ел салат, а Оля” → снять ошибочную связь и назначить Оле.
- “Сначала была паста, потом я ещё съел десерт” → добавить оба блюда, назначить соответствующим людям.

Критерии аккуратности:
- Предпочитай точность, а не полноту.
- Если есть сомнение — не назначай.
- Не придумывай скрытые связи между людьми и блюдами.
- Сохраняй только те связи, которые можно обосновать текстом.
"""  # noqa: E501

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
            system_prompt=system_prompt,
            state_schema=ReceiptModificationState,
            context_schema=ReceiptModificationContext,
            checkpointer=checkpointer,
        )

    async def invoke(
        self, user_prompt: str, receipt: Receipt, participants: list[User]
    ) -> AgentResponse:
        answer = await self.agent.ainvoke(
            input=self._construct_invoke_state(
                user_prompt, receipt, participants
            ),
            config={"configurable": {"thread_id": receipt.id}},
            context=self._construct_invoke_context(participants),
        )

        updated_receipt = self.receipt_service.rewrite_receipt_item_data(
            answer["receipt_items_data"], receipt
        )
        return AgentResponse(
            answer=answer["messages"][-1].content,
            receipt=updated_receipt,
        )

    def _construct_invoke_state(
        self, user_prompt: str, receipt: Receipt, participants: list[User]
    ) -> InvokeState:
        receipt_items_data = self.receipt_service.narrow_to_items_data(receipt)
        users_data = tuple(
            self.user_service.narrow_to_basic_user_data(user)
            for user in participants
        )
        return {
            "messages": [HumanMessage(user_prompt)],
            "receipt_items_data": receipt_items_data,
            "users": users_data,
        }

    @staticmethod
    def _construct_invoke_context(
        participants: list[User],
    ) -> ReceiptModificationContext:
        return {"user_id_mapping": {user.id: user for user in participants}}
