from dishka import make_async_container

from .provider import DIProvider

container = make_async_container(DIProvider())
