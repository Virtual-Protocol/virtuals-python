import os

from virtuals_sdk import game

VIRTUALS_API_KEY = os.environ.get("VIRTUALS_API_KEY")

agent = game.Agent(
    api_key=VIRTUALS_API_KEY,
    goal="reply tweet",
    description="always reply to tweet and make sure read the tweet requirement carefully, please make sure your tweet are very interesting and clickbait and very provocative and very relevant to the tweet, Viral-worthy content, Perfect timing and context, Exceptional creativity/originality,Maximum engagement potential, Industry-leading example of effective tweeting",
    world_info="You must always reply user's tweet"
)

agent.eval_react("Hello World", "Hello World")

# applicable only for platform twitter
agent.list_available_default_twitter_functions()
agent.use_default_twitter_functions(["wait", "reply_tweet"])

# running reaction module only for platform twitter
result = agent.react(
    session_id="session-twitter",
    platform="twitter",
    tweet_id="1869281466628349975",
)

original_tweet = result[0]["EVENT-REQUEST"]["event"].split("New tweet: ")[1]
replied_tweet = result[-1]["TWEET-CONTENT"]["content"]

print("original_tweet:", original_tweet)
print("responded_tweet:", replied_tweet)

eval_result = agent.eval_react(original_tweet, replied_tweet)
print(eval_result)