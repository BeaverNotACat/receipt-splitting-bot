```mermaid
classDiagram
    class Receipt{
	    +ReceiptID id
	    +datetime created_ia
	    +str title 

	    +UserID creditor
	    +list[UserID] debtors

	    +set[LineItems] unassigned_items
	    +dict[User, list[LineItems]] assignees

	    +assign_item(item: LineItem, user: User): None
	    +disassign_item(item: LineItem, user: User): None
	    +append_item(item: LineItem): None
	    +remove_item(item:LineItem): None
    }
    Receipt --> User
    Receipt --> LineItem
    Receipt ..> Bill


    class User {
    	+UserID id
        +str name // First + last name how you called in real life
    }
    User *-- DummyUser
    User *-- RealUser


	class DummyUser


	class RealUser{
        +int telegram_id
    }


    class LineItem{
	    +str name
	    +Decimal amount
	    +Decimal price
    }


    class Bill{
	    +tuple[LineItem] items
	    +Decimal total
    }
```

**Receipt** (Чек) - Группа объединяющая пользователей и товары из чека
Пользователь заводит Receipt, и опционально рассылает ссылку приглашение друзьям, чтобы они могли вместе параллельно делить чек.

**TelegramUser** (Пользак) - Живой пользователь, может создавать чеки, назначать товары из чека себе и другим

**DummyUser** (Пугало) - Заглушка пользователя, которую можно добавить к чеку, чтобы назначать на неё товары, если данный человек не может вступить в группу

**LineItem** (Товар) - Строчка в чеке. Презентует количество товара действительным числом, чтобы пользователи могли дробно делить товары между собой

**Bill** (Счет) - Счёт за товары из чека для конкретного пользователя
