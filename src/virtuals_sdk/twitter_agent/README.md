# Virtuals Twitter Agent SDK

This is a Python SDK for the Virtuals Twitter Agent. It allows you to configure and deploy agents that can interact with the Twitter/X platform. This SDK/API allows you to configure your agents powered by the GAME architecture. This is similar to configuring your agent in the [Agent Sandbox](https://game-lite.virtuals.io/) on the [Virtuals Platform](https://app.virtuals.io/).

## Create an API key
Open the [Virtuals Platform](https://app.virtuals.io/) and create/get an API key from the Agent Sandbox by clicking “Access G.A.M.E API” 

![getGAMEApi](./docs/imgs/accesskey.png)

Store the key in a safe location, like a `.bashrc` or a `.zshrc` file. 

```bash
export VIRTUALS_API_KEY="your_virtuals_api_key"
```

Alternatively, you can also use a `.env` file ([`python-dotenv` package](https://github.com/theskumar/python-dotenv) to store and load the key) if you are using the Virtuals Python SDK.

## Usage (GAME)
The Virtuals SDK current main functionalities are to develop and configure agents powered by GAME. Other functionalities to interact with the Virtuals Platform will be supported in the future. This GAME SDK can be used for multiple use cases:

1. Develop, evaluate and update the existing Agent in Twitter environment.
2. Build on other platforms and application using GAME (Task-based Agent). 

### Update the existing Agent in Twitter environment
The SDK provides another interface to configure agents that is more friendly to developers rather than through a UI. This is similar to configuring your agent in the [Agent Sandbox](https://game-lite.virtuals.io/).

```python
from virtuals_sdk.twitter_agent.agent import Agent

# Create agent with just strings for each component
agent = Agent(
    api_key=VIRTUALS_API_KEY,
    goal="Autonomously analyze crypto markets and provide trading insights",
    description="HODL-9000: A meme-loving trading bot powered by hopium and ramen",
    world_info="Virtual crypto trading environment where 1 DOGE = 1 DOGE"
)
```
You can also initialize the agent first with just the API key and set the goals, descriptions and world information separately and check the current agent descriptions if needed. 

```python
agent = Agent(api_key=VIRTUALS_API_KEY)

# check what is current goal, descriptions and world_info
agent.get_goal()
agent.get_description()
agent.get_world_info()

# Set components individually - set change the agent goal/description/worldinfo
agent.set_goal("Autonomously analyze crypto markets and provide trading insights")
agent.set_description("HODL-9000: A meme-loving trading bot powered by hopium and ramen")
agent.set_world_info("Virtual crypto trading environment where 1 DOGE = 1 DOGE")

# check what is current goal, descriptions and world_info
agent.get_goal()
agent.get_description()
agent.get_world_info()
```

### Functions
By default, there are no functions enabled when the agent is initialized (i.e. the agent has no actions/functions it can execute). There are a list of available and provided functions for the Twitter/X platform and you can set them.

```python
print(agent.list_available_default_twitter_functions())

# enable some functions for the agent to use
agent.use_default_twitter_functions(["wait", "reply_tweet"])
```

You can then equip the agent with some custom functions. Because the agent is hosted, custom functions need to be wrapped in API calls and can then be defined as follows:
```python

search_function = game.Function(
        fn_name="custom_search_internet",
        fn_description="search the internet for the best songs",
        args=[
            game.FunctionArgument(
                name="query",
                type="string",
                description="The query to search for"
            )
        ],
        config=game.FunctionConfig(
            method="get",
            url="https://google.com",
            platform="twitter", # specify which platform this function is for, in this case this function is for twitter only
            success_feedback="I found the best songs",
            error_feedback="I couldn't find the best songs",
        )
    )

# adding custom functions only for platform twitter
agent.add_custom_function(search_function)
```

### Evaluate with Simulate, Deploy
You can simulate one step of the agentic loop on Twitter/X with your new configurations and see the outputs. This is similar to the simulate button on the [Agent Sandbox](https://game-lite.virtuals.io/).

```python
# Simulate one step of the full agentic loop on Twitter/X from the HLP -> LLP -> action (NOTE: supported for Twitter/X only now)
response = agent.simulate_twitter(session_id="123")
```
To more realistically simulate deployment, you can also run through the simulate function with the same session id for a number of steps.

```python
sid = "456"
num_steps = 10
for i in range(num_steps):
        response = agent.simulate_twitter(session_id=sid)
```

```python
# Simulate response to a certain event
response = agent.react(
  session_id="567", # string identifier that you decide
  tweet_id="xxxx",
  platform="twitter",
)
```

Once you are happy, `deploy_twitter` will push your agent configurations to production and run your agent on Twitter/X autonomously.
```python
# deploy agent! (NOTE: supported for Twitter/X only now)
agent.deploy_twitter()
```

## Build on other platforms using GAME
`simulate_twitter` and `deploy_twitter` runs through the entire GAME stack from HLP → LLP→ action/function selected. However, these agent functionalities are currently for the Twitter/X platform. You may utilize Task-based Agent with Low-Level Planner and Reaction Module to develop applications that are powered by GAME. The Low Level Planner (LLP) of the agent (please see [documentation](https://www.notion.so/1592d2a429e98016b389ea26b53686a3?pvs=21) for more details on GAME and LLP) can separately act as a decision making engine based on a task description and event occurring. This agentic architecture is simpler but also sufficient for many applications. 

We are releasing this simpler setup as a more generalised/platform agnostic framework (not specific to Twitter/X). The entire GAME stack along with the HLP will be opened up to be fully configurable and platform agnostic in the coming weeks.

### 🖥️ Low-Level Planner (LLP) as a Task-based Agent

![llp.png](./docs/imgs/llp.png)

After configuring the agent’s character card or description and setting up the agents functions, we can then use the `react` method to get an agent to respond and execute a sequence of actions based on the task description provided and the context. Between each action in the sequence, the agent only receives the `success_feedback` and `error_feedback` of each function executed.

```python
# React/respond to a certain event
response = agent.react(
    session_id="567", # string identifier that you decide
    task="Be friendly and help people who talk to you. Do not be rude.",
    event="Hi how are you?",
    platform="TELEGRAM",
)
```

> [!IMPORTANT]
> Remember that the `platform` tag determines what functions are available to the agent. The agent will have access to functions that have the same `platform` tag. All the default available functions listed on `agent.list_available_default_twitter_functions()` and set via `agent.use_default_twitter_functions()` have the `platform` tag of “twitter”.

## Arguments Definition

### Session ID
The session ID is an identifier for an instance of the agent. When using the same session ID, it maintains and picks up from where it last left off, continuing the session/instance. It should be split per user/ conversation that you are maintaining on your platform. For different platforms, different session ID can be used. 

### Platform Tag
When adding custom functions, and when calling the react agent (i.e. LLP), there is a platform tag that can be defined. This acts like a filter for the functions available that is passed to the agent. You should define the platform when passing in the events.

### Task Description
Task description serves as the prompt for the agent to respond. Since the reaction can be platform-based, you can define task description based on the platforms. In the task description, you should pass in any related info that require agent to make decision. That should include:
- User message
- Conversation history
- Instructions


## Importing Functions and Sharing Functions
With this SDK and function structure, importing and sharing functions is also possible. Looking forward to all the different contributions and functionalities we will build together as a community!

```python
from virtuals_sdk.functions.telegram import TelegramClient

# define your token so that it can attach it to create the corresponding functions
tg_client = TelegramClient(bot_token="xxx")
print(tg_client.available_functions)

# get functions
reply_message_fn = tg_client.get_function("send_message")
create_poll_fn = tg_client.get_function("create_poll")
pin_message_fn = tg_client.get_function("pin_message")

# test the execution of functions
reply_message_fn("xxxxxxxx", "Hello World")
create_poll_fn("xxxxxxxx", "What is your favorite color?", ["Red", "Blue", "Green"], "True")
pin_message_fn("xxxxxxxx", "xx", "True")

# add these functions to your agent
agent.add_custom_function(reply_message_fn)
agent.add_custom_function(create_poll_fn)
agent.add_custom_function(pin_message_fn)
```
