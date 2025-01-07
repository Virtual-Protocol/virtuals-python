from typing import Any, Dict, Optional, List, Union, Sequence, Callable, Tuple
from pydantic import BaseModel, Field
from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Argument(BaseModel):
    name: str
    description: str
    type: Optional[Union[List[str], str]] = None
    optional: Optional[bool] = False

class FunctionResultStatus(str, Enum):
    DONE = "done"
    FAILED = "failed"

class FunctionResult(BaseModel):
    action_id: str
    action_status: FunctionResultStatus
    feedback_message: Optional[str] = None
    info: Optional[Dict[str, Any]] = None

class Function(BaseModel):
    fn_name: str
    fn_description: str
    args: List[Argument]
    hint: Optional[str] = None
    
    # Make executable required but with a default value
    executable: Callable[..., Tuple[FunctionResultStatus, str, dict]] = Field(
        default_factory=lambda: Function._default_executable
    )

    def get_function_def(self):
        return self.model_dump(exclude={'executable'})

    @staticmethod
    def _default_executable(**kwargs) -> Tuple[FunctionResultStatus, str]:
        """Default executable that does nothing"""
        return FunctionResultStatus.DONE, "Default implementation - no action taken", {}
    
    def execute(self, **kwds: Any) -> FunctionResult:
        """Execute the function using arguments from GAME action."""
        fn_id = kwds.get('fn_id')
        args = kwds.get('args', {})

        try:
            # Extract values from the nested dictionary structure
            processed_args = {}
            for arg_name, arg_value in args.items():
                if isinstance(arg_value, dict) and 'value' in arg_value:
                    processed_args[arg_name] = arg_value['value']
                else:
                    processed_args[arg_name] = arg_value
                    
            # print("Processed args: ", processed_args)
            # execute the function provided
            status, feedback, info = self.executable(**processed_args)

            return FunctionResult(
                action_id=fn_id,
                action_status=status,
                feedback_message=feedback,
                info=info,
            )
        except Exception as e:
            return FunctionResult(
                action_id=fn_id,
                action_status=FunctionResultStatus.FAILED,
                feedback_message=f"Error executing function: {str(e)}",
                info={},
            )

# Different ActionTypes returned by the GAME API
class ActionType(Enum):
    CALL_FUNCTION = "call_function"
    CONTINUE_FUNCTION = "continue_function"
    WAIT = "wait"
    GO_TO = "go_to"


## set of different data structures required by the ActionResponse returned from GAME ##
@dataclass(frozen=True)
class HLPResponse:
    plan_id: str
    observation_reflection: str
    plan: Sequence[str]
    plan_reasoning: str
    current_state_of_execution: str
    change_indicator: Optional[str] = None
    log: Sequence[dict] = field(default_factory=list)


@dataclass(frozen=True)
class LLPResponse:
    plan_id: str
    plan_reasoning: str
    situation_analysis: str
    plan: Sequence[str]
    change_indicator: Optional[str] = None
    reflection: Optional[str] = None


@dataclass(frozen=True)
class CurrentTaskResponse:
    task: str
    task_reasoning: str
    location_id: str = field(default="*not provided*")
    llp: Optional[LLPResponse] = None


@dataclass(frozen=True)
class AgentStateResponse:
    hlp: Optional[HLPResponse] = None
    current_task: Optional[CurrentTaskResponse] = None

# ActionResponse format returned from GAME API call
class ActionResponse(BaseModel):
    """
    Response format from the GAME API when selecting an Action
    """
    action_type: ActionType
    agent_state: AgentStateResponse
    action_args: Optional[Dict[str, Any]] = None

