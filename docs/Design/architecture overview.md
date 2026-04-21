## Objectives
- **System must be universal** 
  We are testing concept at current stage. Telegram bot API to easily get chats and media files support. But in perspective our *core* must be ready for integration into any chatting platform.
- **System must be extendable**
  Open-closed principle is enforsed and coupling must be minimal. So we can adapt to specific requirements and be sure in our stability
- **System must be stable**
  Laggy, buggy or software with unintuitive limitations will push away customers and potential command to use our project. Currently there are to so many *AI startups* of any kind, so we need advante in quality
- **Scalability should not be an issue**
  LLM agents may cause unpreventable overhead with extra tool calls/high network usage. System should let us to scale, but also scaling may requier additional infrastructire, that we can't get now bacuse of work under business features.

## Key points
### DDD
Both agent and backend needs to be provided with enforsed business rules.
Operations with key entitines especially **receipts** is described into domain layer to provide consistent behavior.
Also *strategical points* of DDD gives us profits of having same language for LLM prompting and development process.

You can see our entities at `src/domain` module
### Hexagonal architecture
- Separate presentation layer gives us universality of the system. We can add new user *interface* in short time. REST API, GRPC or another kind of bot API's.
- Separate adapters allows us to experiment with different agent approaches easily and gives third-party users to rewrite instrasructure intergrations to their requierements.

Let's take a closer look at the project file tree
```
src/
├── domain             # Fixed entities data and behavior for whole project
│   ├── exceptions
│   ├── models
│   ├── services
│   └── value_objects
├── application
│   ├── common         # Infra interfaces with DTOs to lower coupling
│   │   └── ...
│   └── ...            # Business interactors with entities and abstract infra
├── adapters           # Infrastructure implimentations
│   └── ...
└── presentation
    ├── dependencies   # Providers of infra implentation to Business interactors
    │   └── ...
    └── telegram       # Telegram bot logic that uses Business interactors
        └── ...

```
### Dependency injections
Some scnearios requires wide range of infrastructire adapters, for example here are approximate dependencies for agent chat
```
agent: AgentI
ocr: OpticalCharacterRecognizerI
asr: SpeechRecognizerI
user_provider: UserProviderI
receipt_db_gateway: ReceiptGatewayI
user_db_gateway: UserReaderI
transaction_manager: TransactionManagerI
```
And any of this classes will have their own dependencies.

Classic dependencies management creates a decent amount of code volume that will create extra points of failure.
Less code - less mistakes will happen. To reduce dependencies code we use DI container, especially `dishka`
### Rich typing
In classical paradigma user id is UUID and receipt id is UUID. So requesting receipt with user id will be discovered only on testing stage.
But type checking can such find logical bugs if we will provide enouth info to it.

Thats why `src/domain/value_objects.py` is focused not only on new data types, but on labeling existing one
