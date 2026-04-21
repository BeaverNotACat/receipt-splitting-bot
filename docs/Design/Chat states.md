# States
## /start
```mermaid
stateDiagram-v2
    state is_user_registered
	
    [*] --> /start
    /start --> is_user_registered
    is_user_registered --> AskNickname: False
    AskNickname --> RegisterUser
    RegisterUser --> ProfileScreen
    is_user_registered --> ProfileScreen: True
```

## start={uuid}
```mermaid
stateDiagram-v2
    state is_user_registered
	state is_user_agree
	
    [*] --> /start=uuid
    /start=uuid --> is_user_registered
    is_user_registered --> AskNickname: False
    AskNickname --> RegisterUser
    RegisterUser --> ShowReceiptInfo
    is_user_registered --> ShowReceiptInfo: True
    ShowReceiptInfo --> AskUserJoinReceipt
    AskUserJoinReceipt --> is_user_agree
    is_user_agree --> JoinUser: True
    is_user_agree --> ProfileScreen: False
    JoinUser --> ReceiptChatScreen
```
# Dialogs details
## Registration Flow:
1. Asks nickname
2. Collect chat_id
3. call Register User interactor 
## ReceiptOnboardFlow:
1. Shows receipt title, creditor nickname
2. Asks are you shure with nuttons yes/no
3. Adds user to receipt or 
