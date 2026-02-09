from dishka import Provider, Scope

from src.application.real_user.register import RegisterUser
from src.application.receipt.create import CreateReceipt
from src.application.receipt.get import GetReceipt
from src.application.receipt.join import JoinReceipt
from src.application.receipt.list import ListReceipts

interactors_provider = Provider(Scope.REQUEST)
interactors_provider.provide(RegisterUser)
interactors_provider.provide(CreateReceipt)
interactors_provider.provide(GetReceipt)
interactors_provider.provide(JoinReceipt)
interactors_provider.provide(ListReceipts)
