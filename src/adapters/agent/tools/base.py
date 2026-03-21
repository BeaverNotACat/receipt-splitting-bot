from langchain.tools import ToolRuntime

from src.adapters.agent.context import ReceiptModificationContext
from src.adapters.agent.state import ReceiptModificationState

EmptyGoTo = tuple[()]

ModifyReceiptRuntime = ToolRuntime[
    ReceiptModificationContext, ReceiptModificationState
]
