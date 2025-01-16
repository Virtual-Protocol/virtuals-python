from virtuals_sdk.game.agent import Agent, WorkerConfig
from virtuals_sdk.game.custom_types import Function, Argument
from virtuals_sdk.game.custom_types import FunctionResult, FunctionResultStatus
from typing import Tuple

game_api_key=""

# the get_worker_state_fn and the get_agent_state_fn can be the same function or diffferent
# each worker can also have a different get_worker_state_fn and maintain their own state
# or they can share the same get_worker_state_fn and maintain the same state

def get_worker_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    """
    This function will get called at every step of the workers execution to form the agent's state.
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

def get_agent_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    """
    This function will get called at every step of the agent's execution to form the agent's state.
    It will take as input the function result from the previous step.
    """

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

def throw_fruit(object: str, **kwargs) -> Tuple[FunctionResultStatus, str, dict]:
    """
    Function to throw fruits.
    """
    fruits = {"apple", "banana", "orange", "pear", "mango", "grape"}
    
    if not object:
        return FunctionResultStatus.ERROR, "No fruit specified", {}
    
    if object.lower() in fruits:
        return FunctionResultStatus.DONE, f"Successfully threw the {object} across the room!", {}
    return FunctionResultStatus.ERROR, f"Cannot throw {object} - not a fruit", {}

def throw_furniture(object: str, **kwargs) -> Tuple[FunctionResultStatus, str, dict]:
    """
    Function to throw furniture.
    """
    furniture = {"chair", "table", "stool", "lamp", "vase", "cushion"}
    
    if not object:
        return FunctionResultStatus.ERROR, "No furniture specified", {}
    
    if object.lower() in furniture:
        return FunctionResultStatus.DONE, f"Powerfully threw the {object} across the room!", {}
    return FunctionResultStatus.ERROR, f"Cannot throw {object} - not a furniture item", {}


# create functions for each executable
take_object_fn = Function(
    fn_name="take",
    fn_description="Take object",
    args=[Argument(name="object", type="item", description="Object to take")],
    executable=take_object
)

sit_on_object_fn = Function(
    fn_name="sit",
    fn_description="Sit on object",
    args=[Argument(name="object", type="sittable", description="Object to sit on")],
    executable=sit_on_object
)

throw_object_fn = Function(
    fn_name="throw",
    fn_description="Throw any object",
    args=[Argument(name="object", type="item", description="Object to throw")],
    executable=throw_object
)

throw_fruit_fn = Function(
    fn_name="throw_fruit",
    fn_description="Throw fruit only",
    args=[Argument(name="object", type="item", description="Fruit to throw")],
    executable=throw_fruit
)

throw_furniture_fn = Function(
    fn_name="throw_furniture",
    fn_description="Throw furniture only",
    args=[Argument(name="object", type="item", description="Furniture to throw")],
    executable=throw_furniture
)


# Create the specialized workers
fruit_thrower = WorkerConfig(
    id="fruit_thrower",
    worker_description="A worker specialized in throwing fruits ONLY with precision",
    get_state_fn=get_worker_state_fn,
    action_space=[take_object_fn, sit_on_object_fn, throw_fruit_fn]
)

furniture_thrower = WorkerConfig(
    id="furniture_thrower",
    worker_description="A strong worker specialized in throwing furniture",
    get_state_fn=get_worker_state_fn,
    action_space=[take_object_fn, sit_on_object_fn, throw_furniture_fn]
)

# Create agent with both workers
chaos_agent = Agent(
    api_key=game_api_key,
    name="Chaos",
    agent_goal="Conquer the world by causing chaos.",
    agent_description="You are a mischievous master of chaos is very strong but with a very short attention span, and not so much brains",
    get_agent_state_fn=get_agent_state_fn,
    workers=[fruit_thrower, furniture_thrower]
)

# # interact and instruct the worker to do something
# chaos_agent.get_worker("fruit_thrower").run("make a mess and rest!")

# # compile and run the agent - if you don't compile the agent, the things you added to the agent will not be saved
chaos_agent.compile()
chaos_agent.run()