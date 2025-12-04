## Registration
```mermaid
sequenceDiagram
    participant User
    participant Bot
    User ->> Bot: /start
    Bot ->> User: Asks IRL nickname
    User ->> Bot: Nickname
    Bot -->> User: Bot description and command panel
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
    Bot -->> User: Asks receipt name so user could identify it later
    User ->> Bot: Some name
    Bot -->> User: Invite link and new command panel
```
**Command panel**
- Add dummy user(Добавить виртуального участника)
- Return to main menu
## Adding users to receipt
### Dummy user case
```mermaid
sequenceDiagram
    participant User
    participant Bot
    User ->> Bot: Taps "Add dummy user" on panel
    Bot -->> User: Asks dummy user name
    User ->> Bot: Writes some name
    Bot -->> User: Adds dummy user and writes success message
```
### Real user case
```mermaid
sequenceDiagram
	participant User
    participant New user
    participant Bot

    User ->> New user: Sends message with invite link
    New user ->> Bot: Follows link
    Bot <<->> New user: Registration flow if nessesary
    Bot -->> New user: Command panel
```

## Receipt lines 
**Chat options**
Users  send natural language messages to bot. 
We assume voice messages and photos by using wisper and prl
Our bot tools:
- Add unassigned lines
- Assign line to user
- Unassign line from user