from virtuals_sdk.game.worker import Worker
from virtuals_sdk.game.custom_types import Function, Argument
from virtuals_sdk.game.custom_types import FunctionResult, FunctionResultStatus
from typing import Tuple

game_api_key=""

def get_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    """
    This function will get called at every step of the agent's execution to form the agent's state.
    It will take as input the function result from the previous step.
    """
    # dict containing info about the function result as implemented in the executable
    info = function_result.info 

    # example of fixed state (function result info is not used to change state) - the first state placed here is the initial state
    init_state = {
        "objects": [
            {"name": "apple", "description": "A red apple", "type": ["item", "food"]},
            {"name": "banana", "description": "A yellow banana", "type": ["item", "food"]},
            {"name": "orange", "description": "A juicy orange", "type": ["item", "food"]},
            {"name": "chair", "description": "A chair", "type": ["sittable"]},
            {"name": "table", "description": "A table", "type": ["sittable"]},
        ]
    }

    if current_state is None:
        # at the first step, initialise the state with just the init state
        new_state = init_state
    else:
        # do something with the current state input and the function result info
        new_state = init_state # this is just an example where the state is static

    return new_state

def take_object(object: str, **kwargs) -> Tuple[FunctionResultStatus, str, dict]:
    """
    Function to take an object from the environment.
    
    Args:
        object: Name of the object to take
        **kwargs: Additional arguments that might be passed
    """
    if object:
        return FunctionResultStatus.DONE, f"Successfully took the {object}", {}
    return FunctionResultStatus.FAILED, "No object specified", {}


def throw_object(object: str, **kwargs) -> Tuple[FunctionResultStatus, str, dict]:
    """
    Function to throw an object.
    
    Args:
        object: Name of the object to throw
        **kwargs: Additional arguments that might be passed
    """
    if object:
        return FunctionResultStatus.DONE, f"Successfully threw the {object}", {}
    return FunctionResultStatus.FAILED, "No object specified", {}


def sit_on_object(object: str, **kwargs) -> Tuple[FunctionResultStatus, str, dict]:
    """
    Function to sit on an object.
    
    Args:
        object: Name of the object to sit on
        **kwargs: Additional arguments that might be passed
    """
    sittable_objects = {"chair", "bench", "stool", "couch", "sofa", "bed"}
    
    if not object:
        return FunctionResultStatus.FAILED, "No object specified", {}

    if object.lower() in sittable_objects:
        return FunctionResultStatus.DONE, f"Successfully sat on the {object}", {}
    
    return FunctionResultStatus.FAILED, f"Cannot sit on {object} - not a sittable object", {}


# Action space with all executables
action_space = [
    Function(
        fn_name="take", 
        fn_description="Take object", 
        args=[Argument(name="object", type="item", description="Object to take")],
        executable=take_object
    ),
    Function(
        fn_name="throw", 
        fn_description="Throw object", 
        args=[Argument(name="object", type="item", description="Object to throw")],
        executable=throw_object
    ),
    Function(
        fn_name="sit", 
        fn_description="Take a seat", 
        args=[Argument(name="object", type="sittable", description="Object to sit on")],
        executable=sit_on_object
    )
]



worker = Worker(
    api_key=game_api_key,
    description="You are an evil NPC in a game.",
    instruction="Choose the evil-est actions.",  
    get_state_fn=get_state_fn,
    action_space=action_space
)

# interact and instruct the worker to do something
# worker.run("what would you do to the apple?")
worker.run("take over the world with the things you have around you!")