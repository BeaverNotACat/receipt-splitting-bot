from dishka import Provider, Scope

from src.domain.services.receipt import ReceiptService
from src.domain.services.user import UserService

services_provider = Provider(Scope.APP)
services_provider.provide(UserService)
services_provider.provide(ReceiptService)
