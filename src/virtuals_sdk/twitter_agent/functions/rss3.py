from typing import Dict, List
from virtuals_sdk.game import Function, FunctionConfig, FunctionArgument

class RSS3Client:
    """
    A client for accessing real-time decentralized data via RSS3 Network.
    For the complete API documentation, please refer to [the official RSS3 API documentation](https://docs.rss3.io/guide/developer/api).
    The data is structured to be readily consumable by AI agents.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the RSS3 client.
        
        Args:
            api_key (str): Your RSS3 API key
        """

        self.rss3_endpoint = "https://gi.rss3.io"
        self.api_key = api_key

        self._functions: Dict[str, Function] = {
            "retrieve_account_activities": self._get_account_activities_function(),
            "retrieve_accounts_activities": self._get_accounts_activities_function(),
            "retrieve_single_activity": self._get_account_activities_function(),
        }

    @property
    def available_functions(self) -> List[str]:
        """Get list of available function names."""
        return list(self._functions.keys())
    
    def create_api_url(self, endpoint):
        """Helper function to create full API URL with token"""
        return f"{self.rss3_endpoint}/{endpoint}"

    def get_function(self, fn_name: str) -> Function:
        """
        Get a specific function by name.
        
        Args:
            fn_name: Name of the function to retrieve
            
        Raises:
            ValueError: If function name is not found
            
        Returns:
            Function object
        """
        if fn_name not in self._functions:
            raise ValueError(f"Function '{fn_name}' not found. Available functions: {', '.join(self.available_functions)}")
        return self._functions[fn_name]

    def _get_account_activities_function(self) -> Function:

        # Retrieve Activity Function
        retrieve_activity = Function(
            fn_name="retrieve_account_activities",
            fn_description="Retrieve a list of activities for a specific decentralized account, such as a blockchain wallet address or a Mastodon account.",
            args=[
                FunctionArgument(
                    name="account",
                    description="Unique identifier for the decentralized account.",
                    type="string"
                ),
            ],
            config=FunctionConfig(
                method="get",
                url=self.create_api_url("decentralized/{{account}}"),
                platform="rss3",
                headers={"Content-Type": "application/json", "Authorization": f"Virtuals Bot {self.api_key}"},
                success_feedback="Activities retrieved successfully. Activities: {{response.data}}",
                error_feedback="Failed to retrieve activities: {{response.error}}"
            )
        )

        return retrieve_activity

    def _get_accounts_activities_function(self) -> Function:

        # Retrieve Activity Function
        retrieve_activity = Function(
            fn_name="retrieve_accounts_activities",
            fn_description="Retrieve activities for a list of decentralized accounts, such as blockchain wallet addresses or Mastodon accounts.",
            args=[
                FunctionArgument(
                    name="accounts",
                    description="The list of unique identifiers for the decentralized accounts.",
                    type="List[string]"
                ),
            ],
            config=FunctionConfig(
                method="post",
                url=self.create_api_url("decentralized/accounts"),
                platform="rss3",
                headers={"Content-Type": "application/json", "Authorization": f"Virtuals Bot {self.api_key}"},
                payload={
                    "accounts": "{{accounts}}",
                },
                success_feedback="Activities retrieved successfully. Activities: {{response.data}}",
                error_feedback="Failed to retrieve activities: {{response.error}}"
            )
        )

        return retrieve_activity

    def _get_single_activity_function(self) -> Function:

        # Retrieve Activity Function
        retrieve_activity = Function(
            fn_name="retrieve_account_activities",
            fn_description="Retrieve a single activity on a list of decentralized network, such as a blockchain transaction hash.",
            args=[
                FunctionArgument(
                    name="id",
                    description="Unique identifier for the activity.",
                    type="string"
                ),
            ],
            config=FunctionConfig(
                method="get",
                url=self.create_api_url("decentralized/tx/{{id}}"),
                platform="rss3",
                headers={"Content-Type": "application/json", "Authorization": f"Virtuals Bot {self.api_key}"},
                success_feedback="Activity retrieved successfully. Activity: {{response.data}}",
                error_feedback="Failed to retrieve activities: {{response.error}}"
            )
        )

        return retrieve_activity
