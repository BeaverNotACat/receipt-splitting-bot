## /start
```mermaid
sequenceDiagram
    participant User
    participant Bot
    User ->> Bot: /start
    Bot ->> User: Registration: asks IRL nickname
    User ->> Bot: Tells nickname
    Bot ->> User: Bot description and command panel
```
**Command panel**
- Create new receipt
- List your receipts

## Receipt creation
```mermaid
sequenceDiagram
    participant User
    participant Bot
    User ->> Bot: Taps "Create new receipt" on panel
    Bot ->> User: Asks to give some receipt name so user could identify it later
    User ->> Bot: Writes some name
    Bot -->> User: Gives invite link and updates command panel
```
**Command panel**
- Add dummy user(Добавить виртуального участника)
- Return to main menu
## Adding users to receipt
```mermaid
sequenceDiagram
    participant User
    participant Bot
    User ->> Bot: Taps "Add dummy user" on panel
    Bot ->> User: Asks dummy user name
    User ->> Bot: Writes some name
    Bot -->> User: Adds dummy user and writes success message
```

## Receipt lines 
**Chat options**
Users  send natural language messages to bot. 
We assume voice messages and photos by using wisper and prl
Our bot tools:
- Add unassigned lines
- Assign line to user
- Unassign line from user