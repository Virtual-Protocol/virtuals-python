import requests


class GameSDK:
    api_url: str = "https://game-api.virtuals.io/api"
    api_key: str
    eval_api_url: str = "https://api.evaengine.ai/api"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def functions(self):
        """
        Get all default functions
        """
        response = requests.get(
            f"{self.api_url}/functions", headers={"x-api-key": self.api_key})

        if (response.status_code != 200):
            raise Exception(response.json())

        functions = {}

        for x in response.json()["data"]:
            functions[x["fn_name"]] = x["fn_description"]

        return functions

    def simulate(self, session_id: str,  goal: str, description: str, world_info: str, functions: list, custom_functions: list):
        """
        Simulate the agent configuration
        """
        response = requests.post(
            f"{self.api_url}/simulate",
            json={
                "data": {
                    "sessionId": session_id,
                    "goal": goal,
                    "description": description,
                    "worldInfo": world_info,
                    "functions": functions,
                    "customFunctions": [x.toJson() for x in custom_functions]
                }
            },
            headers={"x-api-key": self.api_key}
        )

        if (response.status_code != 200):
            raise Exception(response.json())

        return response.json()["data"]

    def react(self, session_id: str, platform: str, goal: str,
              description: str, world_info: str, functions: list, custom_functions: list,
              event: str = None, task: str = None, tweet_id: str = None):
        """
        Simulate the agent configuration
        """
        url = f"{self.api_url}/react/{platform}"

        payload = {
            "sessionId": session_id,
            "goal": goal,
            "description": description,
            "worldInfo": world_info,
            "functions": functions,
            "customFunctions": [x.toJson() for x in custom_functions]
        }

        if (event):
            payload["event"] = event

        if (task):
            payload["task"] = task
            
        if (tweet_id):
            payload["tweetId"] = tweet_id
            
        print(payload)

        response = requests.post(
            url,
            json={
                "data": payload
            },
            headers={"x-api-key": self.api_key}
        )

        if (response.status_code != 200):
            raise Exception(response.json())

        return response.json()["data"]
    
    def eval_react(self, input_tweet: str, output_tweet: str):
        """
        Evaluate the agent reply
        Checkout your eval dashboard here: https://evaengine.ai/virtuals (import your api key to view)
        """
        response = requests.post(
            f"{self.eval_api_url}/eval/evaluate-tweet",
            headers={"x-api-key": self.api_key},
            json={
                "input_tweet": input_tweet,
                "output_tweet": output_tweet
            }
        )

        if (response.status_code != 200):
            raise Exception(response.json())

        return response.json()

    def deploy(self, goal: str, description: str, world_info: str, functions: list, custom_functions: list, main_heartbeat: int, reaction_heartbeat: int):
        """
        Simulate the agent configuration
        """
        response = requests.post(
            f"{self.api_url}/deploy",
            json={
                "data": {
                    "goal": goal,
                    "description": description,
                    "worldInfo": world_info,
                    "functions": functions,
                    "customFunctions": custom_functions,
                    "gameState" : {
                        "mainHeartbeat" : main_heartbeat,
                        "reactionHeartbeat" : reaction_heartbeat,
                    }
                }
            },
            headers={"x-api-key": self.api_key}
        )

        if (response.status_code != 200):
            raise Exception(response.json())

        return response.json()["data"]
