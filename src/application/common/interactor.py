from typing import TypeVar

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class Interactor[InputDTO, OutputDTO]:
    """
    Buisness logic executor for request-response messaging
    """

    async def __call__(self, context: InputDTO) -> OutputDTO:
        raise NotImplementedError
