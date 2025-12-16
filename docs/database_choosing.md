Our mentor agitated for relational database instead of No-SQL, so lets do some 1 to 1 comparison suitable for our case.

**MongoDB**

| ✅   | fast and intuitive way to implement aggregates | - `Receipt` is a natural **document aggregate**<br>- `unassigned_items`, `assignees`, `debtors` map very cleanly to embedded arrays/maps<br>- single-document atomic updates match DDD aggregate rules perfectly |
| --- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅   | great fit for OLTP read by id + save tasks     |                                                                                                                                                                                                                  |
| ⚠️  | No FK and constrains                           | But in DDD this is already your responsibility                                                                                                                                                                   |
| ⚠️  | No schema                                      |                                                                                                                                                                                                                  |

**PostgreSQL**

| ❌   | unintuitive way to implement aggregates       | <br><br>                                         |
| --- | --------------------------------------------- | ------------------------------------------------ |
| ✅   | Easy to maintain potential complex structures | - Relational queries<br>- Many-to-many relations |
| ✅   | Enforses data                                 | Constrains, schema, FK                           |
| ✅   | OLAP is better                                | **IF** there will be any OLAP (NO)               |

Quick Receipt conсept:
```mermaid
erDiagram
    receipts {
        UUID id PK
        TIMESTAMPTZ created_at
        UUID creditor_id FK
        TEXT title
    }
    receipts ||--|{ debtors: contains
    receipts ||--|{ line_items: contains
    
    debtors {
	    UUID receipt_id FK
	    UUID user_id FK
    }
    
    line_items {
        UUID id PK
        UUID receipt_id FK
        NUMERIC price
        NUMERIC amount
    }
    line_items ||--|| assgnments: connects
    
    assgnments {
    UUID line_item_id FK
    UUID user_id FK
    }
```