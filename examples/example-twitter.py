import os
from virtuals_sdk import game
import json

agent = game.Agent(
    api_key=os.environ.get("VIRTUALS_API_KEY"),
    goal="search for best songs",
    description="Test Description",
    world_info="Test World Info"
)

# applicable only for platform twitter
agent.list_available_default_twitter_functions()
agent.use_default_twitter_functions(["wait", "reply_tweet"])

# adding custom functions only for platform twitter
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
            # specify which platform this function is for, in this case this function is for twitter only
            platform="twitter",
            success_feedback="I found the best songs",
            error_feedback="I couldn't find the best songs",
        )
    )
)

# running reaction module only for platform twitter
agent.react(
    session_id="session-twitter",
    platform="twitter",
    tweet_id="1869281466628349975",
)

# running simulation module only for platform twitter
agent.simulate_twitter(session_id="session-twitter")

# Export out agent.json to upload to game-lite.virtuals.io
agent.export()

# To deploy the agent
agent.deploy_twitter()