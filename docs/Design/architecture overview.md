
## Objectives

- **The system must be universal**  
  We are testing the concept at the current stage. The Telegram Bot API provides an easy way to work with chats and media files, but in the long term, our *core* must be ready for integration with any messaging platform.

- **The system must be extendable**  
  The Open-Closed Principle is enforced, and coupling must be minimal. This allows us to adapt to specific requirements while maintaining system stability.

- **The system must be stable**  
  Laggy or buggy software, or software with unintuitive limitations, will drive away users and potential teams adopting the project. There are too many *AI startups* today, so we need an advantage in quality.

- **Scalability should not be an issue**  
  LLM agents may introduce unpredictable overhead due to additional tool calls and high network usage. The system should allow us to scale, although scaling may require infrastructure that is not currently available due to a focus on business features.
## Key points
### DDD
Both the agent and the backend must enforce business rules.  
Operations on key entities, especially **receipts**, are defined in the domain layer to ensure consistent behavior.  

Additionally, the *strategic design* aspects of DDD provide the benefit of a shared language between LLM prompting and the development process.

You can find the entities in the `src/domain` module.
### Hexagonal architecture
- A separate presentation layer ensures system universality. We can quickly add new user *interfaces*, such as a REST API, gRPC service, or another type of bot API.
- Separate adapters allow us to experiment with different agent approaches and enable third-party users to rewrite infrastructure integrations according to their requirements.

Let's take a closer look at the project file tree:

```
src/
├── domain             # Core entities, data, and behavior
│   ├── exceptions
│   ├── models
│   ├── services
│   └── value_objects
├── application
│   ├── common         # Infrastructure interfaces and DTOs to reduce coupling
│   │   └── ...
│   └── ...            # Business use cases interacting with domain and abstract infrastructure
├── adapters           # Infrastructure implementations
│   └── ...
└── presentation
    ├── dependencies   # Providers of infrastructure implementations for use cases
    │   └── ...
    └── telegram       # Telegram bot logic using application layer
        └── ...
```
### Dependency injection
Some scenarios require a wide range of infrastructure adapters. For example, approximate dependencies for an agent chat:
```
agent: AgentI
ocr: OpticalCharacterRecognizerI
asr: SpeechRecognizerI
user_provider: UserProviderI
receipt_db_gateway: ReceiptGatewayI
user_db_gateway: UserReaderI
transaction_manager: TransactionManagerI
```

Each of these components may also have its own dependencies.

Classic dependency management introduces a significant amount of boilerplate code, increasing the number of potential failure points. Less code means fewer mistakes.  
To reduce this overhead, we use a DI container, specifically `dishka`.
### Rich typing
In a classical paradigm, both user IDs and receipt IDs may be represented as UUIDs. This means that passing a user ID instead of a receipt ID might only be detected during testing.

However, strong typing can catch such logical errors earlier if we provide enough type information.

That’s why `src/domain/value_objects.py` focuses not only on defining new data types, but also on labeling existing ones.