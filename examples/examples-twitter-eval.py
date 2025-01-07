import os
import requests
from virtuals_sdk import game

# Checkout your eval dashboard here: https://evaengine.ai/virtuals (import your api key to view)
def eval_tweet(original_tweet, responded_tweet):
    headers = {
        "x-api-key": "YOUR_API_KEY",  # Replace with actual API key
        "Content-Type": "application/json"
    }
    payload = {
        "input_tweet": original_tweet,
        "output_tweet": responded_tweet
    }
    response = requests.post(
        "https://api.evaengine.ai/api/eval/evaluate-tweet",
        headers=headers,
        json=payload
    )
    return response.json()

agent = game.Agent(
    api_key=os.environ.get("VIRTUALS_API_KEY"),
    goal="reply tweet",
    description="always reply to tweet and make sure read the tweet requirement carefully, please make sure your tweet are very interesting and clickbait and very provocative and very relevant to the tweet, Viral-worthy content, Perfect timing and context, Exceptional creativity/originality,Maximum engagement potential, Industry-leading example of effective tweeting",
    world_info="You must always reply user's tweet"
)

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

eval_result = eval_tweet(original_tweet, replied_tweet)
print(eval_result)