from dishka import AnyOf, Provider, Scope

from src.adapters.database.receipt_gateway import ReceiptGateway
from src.adapters.database.transaction_manager import TransactionManager
from src.adapters.database.user_gateway import UserGateway
from src.application.common.database import (
    ReceiptGatewayI,
    ReceiptReaderI,
    ReceiptSaverI,
)
from src.application.common.database.transaction_manager import (
    TransactionManagerI,
)
from src.application.common.database.user_gateway import (
    UserGatewayI,
    UserReaderI,
    UserSaverI,
)

repositories_provider = Provider(Scope.REQUEST)
repositories_provider.provide(TransactionManager, provides=TransactionManagerI)
repositories_provider.provide(
    UserGateway, provides=AnyOf[UserReaderI, UserSaverI, UserGatewayI]
)
repositories_provider.provide(
    ReceiptGateway,
    provides=AnyOf[ReceiptReaderI, ReceiptSaverI, ReceiptGatewayI],
)
