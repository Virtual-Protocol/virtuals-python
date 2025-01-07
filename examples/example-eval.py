import os

from virtuals_sdk import game

VIRTUALS_API_KEY = os.environ.get("VIRTUALS_API_KEY")

agent = game.Agent(
    api_key=VIRTUALS_API_KEY,
    goal="reply tweet",
    description="always reply to tweet and make sure read the tweet requirement carefully, please make sure your tweet are very interesting and clickbait and very provocative and very relevant to the tweet, Viral-worthy content, Perfect timing and context, Exceptional creativity/originality,Maximum engagement potential, Industry-leading example of effective tweeting",
    world_info="You must always reply user's tweet"
)

# applicable only for platform twitter
agent.list_available_default_twitter_functions()
agent.use_default_twitter_functions(["wait", "reply_tweet"])

# # running reaction module only for platform twitter
# result = agent.react(
#     session_id="session-twitter",
#     platform="twitter",
#     tweet_id="1869281466628349975",
# )

# print("original_tweet:", original_tweet)
# print("responded_tweet:", replied_tweet)

# # Checkout your eval dashboard here: https://evaengine.ai/virtuals (import your api key to view)
# eval_result = agent.eval_react(result)
# print(eval_result)

# Run multiple test to get average eval score
eval_results = []
for i in range(2):
    result = agent.react(
        session_id="session-twitter",
        platform="twitter",
        tweet_id="1869281466628349975",
    )
    eval_result = agent.eval_react(result)
    eval_results.append(eval_result)

# Calculate averages from eval_results
final_scores = [result['final_score'] for result in eval_results]
truth_scores = [result['truth']['score'] for result in eval_results]
accuracy_scores = [result['accuracy']['score'] for result in eval_results]
creativity_scores = [result['creativity']['score'] for result in eval_results] 
engagement_scores = [result['engagement']['score'] for result in eval_results]

print(f"Average scores across {len(eval_results)} evaluations:")
print(f"Final Score: {(sum(final_scores) / len(final_scores)):.2f}")
print(f"Truth Score: {(sum(truth_scores) / len(truth_scores)):.2f}")
print(f"Accuracy Score: {(sum(accuracy_scores) / len(accuracy_scores)):.2f}") 
print(f"Creativity Score: {(sum(creativity_scores) / len(creativity_scores)):.2f}")
print(f"Engagement Score: {sum(engagement_scores) / len(engagement_scores):.2f}")
