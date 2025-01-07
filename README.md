# Virtuals Python SDK Library
The Virtuals Python SDK is a library that allows you interact with the Virtuals Platform.

Currently, this SDK/API allows you to develop your agents powered by the GAME architecture. There are two main functionalities for this SDK:

1. [Twitter Agent](./src/virtuals_sdk/twitter_agent/README.md): The Virtuals Platform offers a out-of-the-box hosted agent that can be used to interact with the Twitter/X platform, powered by GAME. This agent comes with existing functions/actions that can be used to interact with the Twitter/X platform and can be immediately hosted/deployed as you configure it. This is similar to configuring your agent in the [Agent Sandbox](https://game-lite.virtuals.io/) on the [Virtuals Platform](https://app.virtuals.io/) but through a developer-friendly SDK interface.


2. [Custom GAME Agent](./src/virtuals_sdk/game/README.md): This SDK also offers a Python SDK to use the GAME architecture in its most fullest and most flexible form. It allows you to develop your own custom agents for any application or platform. The modularity and flexibilty of this SDK allows you to have full control of what the agent sees (state) and can do (actions/functions). Custom functions do not have to be wrapper in API services, but can be defined as just an executable function in Python.
This same flexibility is also provided as a [TypeScript SDK](https://www.npmjs.com/package/@virtuals-protocol/game) if you prefer to develop your agents in TypeScript.

## Documentation
Detailed documentation to better understand the configurable components and the GAME architecture can be found on [here](https://whitepaper.virtuals.io/developer-documents/game-framework).

## Installation
```bash
pip install virtuals_sdk
```

