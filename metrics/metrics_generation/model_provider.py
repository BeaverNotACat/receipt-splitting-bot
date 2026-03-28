from langchain_openrouter import ChatOpenRouter

from src.presentation.dependencies import container
from src.settings import Settings

client = ChatOpenRouter(  # type: ignore[call-arg]
    model="nvidia/nemotron-3-super-120b-a12b:free",
    temperature=0,
    api_key=container.get_sync(Settings).OPENROUTER_API_KEY,
)
