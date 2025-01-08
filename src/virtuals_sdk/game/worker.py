from typing import Any, Callable, Dict, Optional, List
from custom_types import Function, FunctionResult, FunctionResultStatus, ActionResponse, ActionType
from utils import create_agent, create_workers
from utils import post


class Worker:
    """
    A interactable worker agent, that can autonomously complete tasks with its available functions when given a task
    """

    def __init__(
        self,
        api_key: str,
        description: str,  # description of the worker/character card (PROMPT)
        get_state_fn: Callable,
        action_space: List[Function],
        # specific additional instruction for the worker (PROMPT)
        instruction: Optional[str] = "",
    ):

        self._base_url: str = "https://game.virtuals.io"
        self._api_key: str = api_key

        # checks
        if not self._api_key:
            raise ValueError("API key not set")

        self.description: str = description
        self.instruction: str = instruction

        # setup get state function and initial state
        self.get_state_fn = lambda function_result, current_state: {
            "instructions": self.instruction,  # instructions are set up in the state
            # places the rest of the output of the get_state_fn in the state
            **get_state_fn(function_result, current_state),
        }
        dummy_function_result = FunctionResult(
            action_id="",
            action_status=FunctionResultStatus.DONE,
            feedback_message="",
            info={},
        )
        # get state
        self.state = self.get_state_fn(dummy_function_result, None)

        # # setup action space (functions/tools available to the worker)
        # check action space type - if not a dict
        if not isinstance(action_space, dict):
            self.action_space = {
                f.get_function_def()["fn_name"]: f for f in action_space}
        else:
            self.action_space = action_space

        # initialize an agent instance for the worker
        self._agent_id: str = create_agent(
            self._base_url, self._api_key, "StandaloneWorker", self.description, "N/A"
        )

        # persistent variables that is maintained through the worker running
        # task ID for everytime you provide/update the task (i.e. ask the agent to do something)
        self._submission_id: Optional[str] = None
        # current response from the Agent
        self._function_result: Optional[FunctionResult] = None

    def set_task(self, task: str):
        """
        Sets the task for the agent
        """
        set_task_response = post(
            base_url=self._base_url,
            api_key=self._api_key,
            endpoint=f"/v2/agents/{self._agent_id}/tasks",
            data={"task": task},
        )
        # response_json = set_task_response.json()

        # if set_task_response.status_code != 200:
        #     raise ValueError(f"Failed to assign task: {response_json}")

        # task ID
        self._submission_id = set_task_response["submission_id"]

        return self._submission_id

    def _get_action(
        self,
        # results of the previous action (if any)
        function_result: Optional[FunctionResult] = None
    ) -> ActionResponse:
        """
        Gets the agent action from the GAME API
        """
        # dummy function result if None is provided - for get_state_fn to take the same input all the time
        if function_result is None:
            function_result = FunctionResult(
                action_id="",
                action_status=FunctionResultStatus.DONE,
                feedback_message="",
                info={},
            )
        # set up data payload
        data = {
            "environment": self.state,  # state (updated state)
            "functions": [
                f.get_function_def() for f in self.action_space.values()  # functions available
            ],
            "action_result": (
                function_result.model_dump(
                    exclude={'info'}) if function_result else None
            ),
        }

        # make API call
        response = post(
            base_url=self._base_url,
            api_key=self._api_key,
            endpoint=f"/v2/agents/{self._agent_id}/tasks/{self._submission_id}/next",
            data=data,
        )

        return ActionResponse.model_validate(response)

    def step(self):
        """
        Execute the next step in the task - requires a task ID (i.e. task ID)
        """
        if not self._submission_id:
            raise ValueError("No task set")

        # get action from GAME API (Agent)
        action_response = self._get_action(self._function_result)
        action_type = action_response.action_type

        print(f"Action response: {action_response}")
        print(f"Action type: {action_type}")

        # execute action
        if action_type == ActionType.CALL_FUNCTION:
            if not action_response.action_args:
                raise ValueError("No function information provided by GAME")

            self._function_result = self.action_space[
                action_response.action_args["fn_name"]
            ].execute(**action_response.action_args)

            print(f"Function result: {self._function_result}")

            # update state
            self.state = self.get_state_fn(self._function_result, self.state)

        elif action_response.action_type == ActionType.WAIT:
            print("Task completed or ended (not possible)")
            self._submission_id = None

        else:
            raise ValueError(
                f"Unexpected action type: {action_response.action_type}")

        return action_response, self._function_result.model_copy()

    def run(self, task: str):
        """
        Gets the agent to complete the task on its own autonomously
        """

        self.set_task(task)
        while self._submission_id:
            self.step()
