from typing import List, Any, Dict, Optional, Union, Set
from dataclasses import dataclass, asdict
from string import Template
import json
import uuid
import requests
from virtuals_sdk import sdk


@dataclass
class FunctionArgument:
    name: str
    description: str
    type: str
    id: str = None
    
    def __post_init__(self):
        self.id = self.id or str(uuid.uuid4())


@dataclass
class FunctionConfig:
    method: str = "get"
    url: str = ""
    headers: Dict = None
    payload: Dict = None
    success_feedback: str = ""
    error_feedback: str = ""
    isMainLoop: bool = False
    isReaction: bool = False
    headersString: str = "{}"  # Added field
    payloadString: str = "{}"  # Added field
    platform: str = None

    def __post_init__(self):
        self.headers = self.headers or {}
        self.payload = self.payload or {}

        self.headersString = json.dumps(self.headers, indent=4)
        self.payloadString = json.dumps(self.payload, indent=4)


@dataclass
class Function:
    fn_name: str
    fn_description: str
    args: List[FunctionArgument]
    config: FunctionConfig
    hint: str = ""
    id: str = None

    def __post_init__(self):
        self.id = self.id or str(uuid.uuid4())

    def toJson(self):
        return {
            "id": self.id,
            "fn_name": self.fn_name,
            "fn_description": self.fn_description,
            "args": [asdict(arg) for arg in self.args],
            "hint": self.hint,
            "config": asdict(self.config)
        }

    def _validate_args(self, *args) -> Dict[str, Any]:
        """Validate and convert positional arguments to named arguments"""
        if len(args) != len(self.args):
            raise ValueError(f"Expected {len(self.args)} arguments, got {len(args)}")

        # Create dictionary of argument name to value
        arg_dict = {}
        for provided_value, arg_def in zip(args, self.args):
            arg_dict[arg_def.name] = provided_value

            # Type validation (basic)
            if arg_def.type == "string" and not isinstance(provided_value, str):
                raise TypeError(f"Argument {arg_def.name} must be a string")
            elif arg_def.type == "array" and not isinstance(provided_value, (list, tuple)):
                raise TypeError(f"Argument {arg_def.name} must be an array")
            # elif arg_def.type == "boolean" and not isinstance(provided_value, bool):
            #     raise TypeError(f"Argument {arg_def.name} must be a boolean")

        return arg_dict

    def _interpolate_template(self, template_str: str, values: Dict[str, Any]) -> str:
        """Interpolate a template string with given values"""
        # Convert Template-style placeholders ({{var}}) to Python style ($var)
        python_style = template_str.replace('{{', '$').replace('}}', '')
        return Template(python_style).safe_substitute(values)

    def _prepare_request(self, arg_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the request configuration with interpolated values"""
        config = self.config

        # Interpolate URL
        url = self._interpolate_template(config.url, arg_dict)

        # Interpolate payload
        payload = {}
        for key, value in config.payload.items():
            if isinstance(value, str):
                # Handle template values
                template_key = self._interpolate_template(key, arg_dict)
                if value.strip('{}') in arg_dict:
                    # For array and other non-string types, use direct value
                    payload[template_key] = arg_dict[value.strip('{}')]
                else:
                    # For string interpolation
                    payload[template_key] = self._interpolate_template(value, arg_dict)
            else:
                payload[key] = value

        return {
            "method": config.method,
            "url": url,
            "headers": config.headers,
            "data": json.dumps(payload)
        }

    def __call__(self, *args):
        """Allow the function to be called directly with arguments"""
        # Validate and convert args to dictionary
        arg_dict = self._validate_args(*args)

        # Prepare request
        request_config = self._prepare_request(arg_dict)

        # Make the request
        response = requests.request(**request_config)

        # Handle response
        if response.ok:
            try:
                result = response.json()
            except requests.exceptions.JSONDecodeError:
                result = response.text or None
            # Interpolate success feedback if provided
            if hasattr(self.config, 'success_feedback'):
                print(self._interpolate_template(self.config.success_feedback, 
                                              {"response": result, **arg_dict}))
            return result
        else:
            # Handle error
            try:
                error_msg = response.json()
            except requests.exceptions.JSONDecodeError:
                error_msg = {"description": response.text or response.reason}
            if hasattr(self.config, "error_feedback"):
                print(
                    self._interpolate_template(
                        self.config.error_feedback, {"response": error_msg, **arg_dict}
                    )
                )
            raise requests.exceptions.HTTPError(f"Request failed: {error_msg}")


class Agent:
    def __init__(
        self,
        api_key: str,
        goal: str = "",
        description: str = "",
        world_info: str = "",
        main_heartbeat: int = 15,
        reaction_heartbeat: int = 5
    ):
        self.game_sdk = sdk.GameSDK(api_key)
        self.goal = goal
        self.description = description
        self.world_info = world_info
        self.enabled_functions: List[str] = []
        self.custom_functions: List[Function] = []
        self.main_heartbeat = main_heartbeat
        self.reaction_heartbeat = reaction_heartbeat

    def set_goal(self, goal: str):
        self.goal = goal
        return True
    
    def set_description(self, description: str):
        self.description = description
        return True
    
    def set_world_info(self, world_info: str):
        self.world_info = world_info
        return True
    
    def set_main_heartbeat(self, main_heartbeat: int):
        self.main_heartbeat = main_heartbeat
        return True
    
    def set_reaction_heartbeat(self, reaction_heartbeat: int):
        self.reaction_heartbeat = reaction_heartbeat
        return True

    def get_goal(self) -> str:
        return self.goal
    
    def get_description(self) -> str:
        return self.description
    
    def get_world_info(self) -> str:
        return self.world_info

    def list_available_default_twitter_functions(self) -> Dict[str, str]:
        """
        List all of the default functions (currently default functions are only available for Twitter/X platform)
        TODO: will be moved to another layer of abstraction later
        """
        # Combine built-in and custom function descriptions
        return self.game_sdk.functions()

    def use_default_twitter_functions(self, functions: List[str]):
        """
        Enable built-in functions by default
        """
        self.enabled_functions = functions
        return True

    def add_custom_function(self, custom_function: Function) -> bool:
        """
        Add a custom function to the agent
        Custom functions are automatically added and enabled
        """
        # Add to custom functions list
        self.custom_functions.append(custom_function)

        return True

    def simulate_twitter(self, session_id: str):
        """
        Simulate the agent configuration for Twitter
        """
        return self.game_sdk.simulate(
            session_id,
            self.goal,
            self.description,
            self.world_info,
            self.enabled_functions,
            self.custom_functions
        )

    def react(self, session_id: str, platform: str, tweet_id: str = None, event: str = None, task: str = None):
        """
        React to a tweet
        """
        return self.game_sdk.react(
            session_id=session_id,
            platform=platform,
            event=event,
            task=task,
            tweet_id=tweet_id,
            goal=self.goal,
            description=self.description,
            world_info=self.world_info,
            functions=self.enabled_functions,
            custom_functions=self.custom_functions
        )
    
    def eval_react(self, response: List[Dict[str, Any]]):
        """
        Evaluate the agent reply with EvaEngine
        Checkout your eval dashboard here: https://evaengine.ai/virtuals (import your api key to view)
        """
        original_tweet = response[0]["EVENT-REQUEST"]["event"].split("New tweet: ")[1]
        replied_tweet = response[-1]["TWEET-CONTENT"]["content"]
        return self.game_sdk.eval_react(original_tweet, replied_tweet)

    def deploy_twitter(self):
        """
        Deploy the agent configuration
        """
        return self.game_sdk.deploy(
            self.goal,
            self.description,
            self.world_info,
            self.enabled_functions,
            self.custom_functions,
            self.main_heartbeat,
            self.reaction_heartbeat
        )

    def export(self) -> str:
        """Export the agent configuration as JSON string"""
        export_dict = {
            "goal": self.goal,
            "description": self.description,
            "worldInfo": self.world_info,
            "functions": self.enabled_functions,
            "customFunctions": [
                {
                    "id": func.id,
                    "fn_name": func.fn_name,
                    "fn_description": func.fn_description,
                    "args": [asdict(arg) for arg in func.args],
                    "hint": func.hint,
                    "config": asdict(func.config)
                }
                for func in self.custom_functions
            ]
        }
        agent_json = json.dumps(export_dict, indent=4)

        # save to file
        with open('agent.json', 'w') as f:
            f.write(agent_json)

        return agent_json
