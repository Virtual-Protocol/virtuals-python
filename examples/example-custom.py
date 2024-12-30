import os
from virtuals_sdk import game
import json

agent = game.Agent(
    api_key=os.environ.get("VIRTUALS_API_KEY"),
    goal="search for best songs",
    description="Test Description",
    world_info="Test World Info"
)

# running reaction module for other platforms
# adding custom functions for platform specifics
agent.add_custom_function(
    game.Function(
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
            platform="telegram",  # this function will only be used for telegram
            success_feedback="I found the best songs",
            error_feedback="I couldn't find the best songs",
        )
    )
)

# running reaction module only for platform telegram
agent.react(
    session_id="session-telegram",
    # specify the platform telegram
    platform="telegram",
    # specify the event that triggers the reaction
    event="message from user: give me some great music?",
    # specify the task that the agent should do
    task="reply with a music recommendation",
)

# Export out agent.json to upload to game-lite.virtuals.io
agent.export()

# To deploy the agent
agent.deploy_twitter()
