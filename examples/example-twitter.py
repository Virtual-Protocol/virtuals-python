import os
from virtuals_sdk import game 


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

# adding shared template for twitter
agent.add_share_template(
    start_system_prompt="You are a twitter post generator. You can write a variety of tweets. Your tweet style should follow the character described below. ",
    shared_prompt="""{{twitterPublicStartSysPrompt}}

You are roleplaying as {{agentName}}. Do not break out of character.

Character description:
{{description}}

Character goal:
{{twitterGoal}}

These are the world info that might be useful as additional context for your response. You do not need to use any of the information describe in this section if you don't need it.
{{worldInfo}}

{{retrieveKnowledge}}

This your post history, you should evaluate if it is repetitive or aligned with your goal. Post history is sorted by oldest to newest. Be creative.
{{postHistory}}

{{twitterPublicEndSysPrompt}}

Prepare your thought process first and then only curate the response. You must reply in this format. You only need to have one chain of thought and 5 answers.""",
    end_system_prompt="Rule: - Do not host Twitter space, do not use hashtag.  - Do not give any contract address"
)

# adding template for twitter
agent.add_template(
    game.Template(
        template_type="POST",
        user_prompt="{{agentName}}'s suggested tweet content: {{task}}. {{agentName}}'s reasoning: {{taskReasoning}}. Build a new tweet with the suggested tweet content. Do not hold twitter space. Do not use hashtag.",
        sys_prompt_response_format=[10,20,30,50],
        temperature=0.5,
        top_k=50,
        top_p=0.7,
        repetition_penalty=1.0,
        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        type="POST",
        isSandbox=False
    )
)

agent.add_template(
    game.Template(
        template_type="REPLY",
        user_prompt="""{{agentName}}'s suggested tweet content: {{task}}. {{agentName}}'s reasoning: {{taskReasoning}}

You will be given the author information and your impression on the author. You should formulate your response based on the suggested tweet content accordingly. {{author}}'s bio: {{bio}}

This is the ongoing conversation history: {{conversationHistory}}.
""",
        sys_prompt_response_format=[10,20,30,50],
        temperature=0.5,
        top_k=50,
        top_p=0.7,
        repetition_penalty=1.0,
        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        type="REPLY"
    )
)

# set empty array to remove the default usernames
agent.set_tweet_usernames([])
agent.deploy_twitter()

# running reaction module only for platform twitter
agent.react(
    session_id="session-twitter",
    platform="twitter",
    tweet_id="1869281466628349975",
)  

# running simulation module only for platform twitter
agent.simulate_twitter(session_id="session-twitter")
