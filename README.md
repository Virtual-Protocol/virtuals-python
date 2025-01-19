# Virtuals Python SDK Library [WARNING: MIGRATING - WILL BE DEPRECATED]
THIS REPOSITORY WILL NO LONGER BE MAINTAINED AND HAS BEEN MIGRATED OVER TO https://github.com/game-by-virtuals/game-python/tree/main. Please move over to use latest SDK and features.

## Table of Contents
- [About G.A.M.E.](#about-game)
- [About Virtuals Python SDK](#about-virtuals-python-sdk)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [How to Contribute](#how-to-contribute)
- [Documentation](#documentation)
- [Useful Resources](#useful-resources)

The Virtuals Python SDK is a library that allows you interact with the Virtuals Platform.

## About G.A.M.E.
GAME is a modular agentic framework which enables an agent to plan actions and make decisions autonomously based on information provided to it.

Please refer to our [whitepaper](https://whitepaper.virtuals.io/developer-documents/game-framework) for more information and resources.

## About Virtuals Python SDK
Currently, this SDK allows you to develop your agents powered by the GAME architecture in its most fullest and most flexible form.

![New SDK visual](docs/imgs/new_sdk_visual.png)
The python SDK is made up of 3 main components (Agent, Worker, function), each with configurable arguments.

Agent (a.k.a. [high level planner](https://whitepaper.virtuals.io/developer-documents/game-framework/game-overview#high-level-planner-hlp-context))
- Takes in a <b>Goal</b>
  - Drives the agents behaviour through the high level plan which influences the thinking and creation of tasks that would contribute towards this goal
- Takes in a <b>Description</b>
  - Combination of what was previously known as World Info + Agent Description
  - This include a description of the "world" the agent lives in, and the personality and background of the agent

Worker (a.k.a. [low-level planner](https://whitepaper.virtuals.io/developer-documents/game-framework/game-overview#low-level-planner-llp-context)) 
- Takes in a <b>Description</b>
  - Used to control which workers are called by the agent, based on the high-level plan and tasks created to contribute to the goal

Function
- Takes in a <b>Description</b>
  - Used to control which functions are called by the workers, based on each worker's low-level plan
  - This can be any python executable

## Features
- Develop your own custom agents for any application or platform. 
- Ability to control your agents and workers via descriptions (prompts)
- Full control of what the agent sees (state) and can do (actions/functions)
- Ability to fully customise functions. This could include various combinations of programmed logic. For example:
  - Calling an API to retrieve data
  - Calling an API to retrieve data, followed by custom calculations or data processing logic in python code
  - 2 API calls chained together (e.g. calling an API to retrieve web data, and then posting a tweet)

> ### ℹ️ Changes from older python SDK version (prior to 8 Jan 2025)
>![Old SDK visual](docs/imgs/old_sdk_visual.png)
> - Ability to fully customise functions (previously, each function was a single API call)
> - Ability to control the low-level planner via description prompt (previously, only the high-level planner and functions could be controlled via description prompts)
> - The description defined in the agent is equivalent to what was previously known as world information and agent description

## Prerequisites
- Python 3.8 or higher
- pip package manager
- A basic understanding of the GAME framework (refer to our [whitepaper](https://whitepaper.virtuals.io/developer-documents/game-framework))

## Installation
```bash
# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install the package
pip install virtuals_sdk

# Verify installation
python -c "import virtuals_sdk; print(virtuals_sdk.__version__)"
```

## Usage
The SDK provides a simple way to create and configure your agents. Here's a quick example:

```python
from virtuals_sdk import Agent, Worker

# Create an agent
agent = Agent(
    goal="Your agent's goal here",
    description="Your agent's description and world information"
)

# Create a worker
worker = Worker(
    description="Your worker's description"
)

# Start the agent
agent.start()
```

For more detailed examples, please refer to:
- [`test_agent.py`](examples/game/test_agent.py) - Example of agent configuration and usage
- [`test_worker.py`](examples/game/test_worker.py) - Example of worker configuration and usage

## How to Contribute
Contributions are welcome, especially in the form of new plugins! We are working on creating a plugins repo, but in meantime - please contact us via [Twitter](https://x.com/GAME_Virtuals) or [Telegram](https://t.me/virtuaIs_io).

## Documentation
Detailed documentation to better understand the configurable components and the GAME architecture can be found on [here](https://whitepaper.virtuals.io/developer-documents/game-framework).

## Useful Resources
- [TypeScript SDK](https://www.npmjs.com/package/@virtuals-protocol/game): The core logic of this SDK mirrors the logic of this python SDK if you prefer to develop your agents in TypeScript.
- [Twitter Agent](./src/virtuals_sdk/twitter_agent/README.md): The Virtuals Platform offers a out-of-the-box hosted agent that can be used to interact with the Twitter/X platform, powered by GAME. This agent comes with existing functions/actions that can be used to interact with the Twitter/X platform and can be immediately hosted/deployed as you configure it. This is similar to configuring your agent in the [Agent Sandbox](https://game-lite.virtuals.io/) on the [Virtuals Platform](https://app.virtuals.io/) but through a developer-friendly SDK interface.
