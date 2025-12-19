```mermaid
sequenceDiagram
actor User
participant Application #@{ "type" : "boundary" }
participant Agent #@{ "type" : "control" }
participant Interactors/Tooling


loop On text, photo, voice message
    User ->> Application: Sends plain text
    Application ->> Agent: Usses agent to determine actions
    Agent ->> Interactors/Tooling: Exctracts data for interactor and uses it
    Interactors/Tooling -->> Agent: Interactor result
    Agent -->> Application: Generates output or asks additional info
    Application -->> User: Shows generated uotput
end
```
## append_items
**Input:**`line_items: tuple[LineItem]`
**Output:** `None or raises domain exception`
## delete_items
**Input:**`line_items: tuple[LineItem]`
**Output:** `None or raises domain exception`
## assign_items
**Input:**
`user_name: str, line_items: tuple[LineItem]`
or
`dict[str, tuple[LineItem]]`
**Output:** `None or raises exception`
## disassign_items
**Input:**
`user_name: str, line_items: tuple[LineItem]`
or
`dict[str, tuple[LineItem]]`
**Output:** `None or raises exception`

> [!faq] Questions
> - Do we need tool for getting current receipt state, so agent can remind itself or maybe return current state as tool result
> 	- This tool can be us, modificating agent memory on flight.
> - What can we do with two people with the same name
> - Any risks with requiring complex objects like `LineItem`
> -  What  input scheme is better to work with assignees