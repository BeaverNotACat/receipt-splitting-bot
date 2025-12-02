```mermaid
classDiagram
    class Receipt{
	    +Uuid id
	    +UserID reimbursee
	    
	    +list[UserID] debtors
	    +list[LineItems] unassigned_items
	    +dict[User, list[LineItems]] assignees
	    
	    +assign_item(item: LineItem, user: User): None
	    +disassign_item(item: LineItem, user: User): None
	    +make_up_bill(user: UserID): Bill
    }
    Receipt --> User
    Receipt --> LineItem
    Receipt --> Bill


    class User {
    	+id UserID
        +name // First + last name how you called in real life
    }
    User *-- DummyUser
    User *-- TelegramUser


	class DummyUser


	class TelegramUser{
        +telegram_id int
    }


    class LineItem{ // Value obj
	    +name str
	    +price Decimal
    }


    class Bill{ // Value obj
	    +items dict[LineItem, amount]
	    +total Decimal
    }
```

**Receipt** (Чек) - Группа объединяющая пользователей и товары из чека
Пользователь заводит Receipt, и опционально рассылает ссылку приглашение друзьям, чтобы они могли вместе параллельно делить чек.

**TelegramUser** (Пользак) - Живой пользователь, может создавать чеки, назначать товары из чека себе и другим

**DummyUser** (Пугало) - Заглушка пользователя, которую можно добавить к чеку, чтобы назначать на неё товары, если данный человек не может вступить в группу

**LineItem** (Товар) - Строчка в чеке. Презентует 1 конкретную единицу товара, если таких несколько - нужно создавать несколько дубликатов.

**Bill** (Счет) - Счёт за товары из чека для конкретного пользователя
