# OC2 Bot Model

## Discovery and Execution

The bot engine loads `BaseBot` subclasses from Python files under `shared/bots/on`. It skips any class whose name starts with `Base`. It receives OC2 events and calls the corresponding handler. Changes require a bot-engine container restart.

Bots run outside the API's database transaction. Mutating an `Implant` or `BaseTask` received by a handler changes only that in-memory object; use an OC2 service for persistent effects.

Bot instance fields survive between callbacks in one process, but are lost on restart and are not shared across replicas.

## Reliability

- Filter before taking action.
- Design for repeated events when practical.
- Keep network work bounded and avoid scheduling loops.
- Catch expected integration failures close to the failing call.
- Add dependencies to `bot_engine/requirements.txt` and rebuild the image; do not install them at runtime.

## Troubleshooting

Check that:

1. the file is under `shared/bots/on`;
2. the class derives from `BaseBot`;
3. a custom constructor calls `super().__init__()`;
4. imports and dependencies succeed;
5. the bot engine was restarted;
6. logs show module loading and no handler exception.
