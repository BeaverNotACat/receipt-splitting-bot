from langchain_openrouter import ChatOpenRouter

from src.presentation.dependencies import container
from src.settings import OpenRouterSettings

client = ChatOpenRouter(  # type: ignore[call-arg]
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=container.get_sync(OpenRouterSettings).API_KEY,
)
