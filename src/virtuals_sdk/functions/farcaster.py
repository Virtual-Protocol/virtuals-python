from typing import Dict, List
from virtuals_sdk.game import Function, FunctionConfig, FunctionArgument


class FarcasterClient:
    """
    A client for interacting with the Farcaster protocol via the Neynar API.

    Initialize with your API key and signer UUID to create Farcaster API functions.

    Example:
        client = FarcasterClient("your-api-key-here", "your-signer-uuid-here")
        get_user_info = client.get_function("get_user_info")
    """

    BASE_URL = "https://api.neynar.com/v2/farcaster"

    def __init__(self, api_key: str, signer_uuid: str):
        """
        Initialize the Farcaster client with an API key and signer UUID.

        Args:
            api_key (str): Your Neynar API key.
            signer_uuid (str): The UUID of the signer for authenticated requests.
        """
        self.api_key = api_key
        self.signer_uuid = signer_uuid
        self.headers = {
            "x-api-key": f"{self.api_key}",
            "Content-Type": "application/json",
            "accept": "application/json",
        }

        self._functions: Dict[str, Function] = {
            "get_user_info": self._create_get_user_info(),
            "get_user_casts": self._create_get_user_casts(),
            "post_cast": self._create_post_cast(),
            "delete_cast": self._create_delete_cast(),
            "follow_user": self._create_follow_user(),
            "unfollow_user": self._create_unfollow_user(),
            "follow_channel": self._create_follow_channel(),
            "unfollow_channel": self._create_unfollow_channel(),
        }

    @property
    def available_functions(self) -> List[str]:
        """Get list of available function names."""
        return list(self._functions.keys())

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
            raise ValueError(
                f"Function '{fn_name}' not found. Available functions: {', '.join(self.available_functions)}"
            )
        return self._functions[fn_name]

    def create_api_url(self, endpoint: str) -> str:
        """Helper function to create full API URL."""
        return f"{self.BASE_URL}/{endpoint}"

    def _create_get_user_info(self) -> Function:
        """Get User Info Function"""
        return Function(
            fn_name="get_user_info",
            fn_description="Fetch user information by FID.",
            args=[
                FunctionArgument(
                    name="fid", description="Farcaster ID of the user.", type="string"
                )
            ],
            config=FunctionConfig(
                method="get",
                url=self.create_api_url("/user/bulk?fids={{fid}}"),
                platform="farcaster",
                headers=self.headers,
                success_feedback="Got the following info about user with FID '{{fid}}': Username: {{response.users[0].username}} | Bio: {{response.users[0].profile.bio.text}} | Follower Count: {{response.users[0].follower_count}} | Following Count: {{response.users[0].following_count}}",
                error_feedback="Failed to retrieve user information.",
            ),
        )

    def _create_get_user_casts(self) -> Function:
        """Get User Casts Function"""
        return Function(
            fn_name="get_user_casts",
            fn_description="Fetch recent casts from a user.",
            args=[
                FunctionArgument(
                    name="fid", description="Farcaster ID of the user.", type="string"
                ),
                FunctionArgument(
                    name="limit",
                    description="Number of casts to retrieve.",
                    type="integer",
                ),
            ],
            config=FunctionConfig(
                method="get",
                url=self.create_api_url("/feed/user/casts?fid={{fid}}&limit={{limit}}"),
                platform="farcaster",
                headers=self.headers,
                success_feedback="Fetched the following casts from {{fid}}, [-] is separator between casts:: {{#response.casts}} Message: {{text}} | Hash: {{hash}} | Channel ID: {{channel.id}} | Timestamp: {{timestamp}} [-] {{/response.casts}}",
                error_feedback="Failed to retrieve user casts.",
            ),
        )

    def _create_post_cast(self) -> Function:
        """Post Cast Function"""
        return Function(
            fn_name="post_cast",
            fn_description="Post a new cast.",
            args=[
                FunctionArgument(
                    name="text", description="Content of the cast.", type="string"
                ),
                FunctionArgument(
                    name="parent_url",
                    description="Parent url or hash of the parent if replying.",
                    type="string",
                ),
            ],
            config=FunctionConfig(
                method="post",
                url=self.create_api_url("cast"),
                platform="farcaster",
                headers=self.headers,
                payload={
                    "text": "{{text}}",
                    "parent": "{{parent_url}}",
                    "signer_uuid": self.signer_uuid,
                },
                success_feedback="Cast posted successfully.",
                error_feedback="Failed to post cast.",
            ),
        )

    def _create_delete_cast(self) -> Function:
        """Delete Cast Function"""
        return Function(
            fn_name="delete_cast",
            fn_description="Delete a cast by its hash.",
            args=[
                FunctionArgument(
                    name="cast_hash",
                    description="Hash of the cast to delete.",
                    type="string",
                )
            ],
            config=FunctionConfig(
                method="delete",
                url=self.create_api_url("cast"),
                platform="farcaster",
                headers=self.headers,
                payload={
                    "signer_uuid": self.signer_uuid,
                    "target_hash": "{{cast_hash}}",
                },
                success_feedback="Cast deleted successfully.",
                error_feedback="Failed to delete cast.",
            ),
        )

    def _create_follow_user(self) -> Function:
        """Follow User Function"""
        return Function(
            fn_name="follow_user",
            fn_description="Follow a user by their FID.",
            args=[
                FunctionArgument(
                    name="target_fid",
                    description="FID of the user to follow.",
                    type="int",
                )
            ],
            config=FunctionConfig(
                method="post",
                url=self.create_api_url("user/follow"),
                platform="farcaster",
                headers=self.headers,
                payload={
                    "target_fids": ["{{target_fid}}"],
                    "signer_uuid": self.signer_uuid,
                },
                success_feedback="User followed successfully.",
                error_feedback="Failed to follow user.",
            ),
        )

    def _create_unfollow_user(self) -> Function:
        """Unfollow User Function"""
        return Function(
            fn_name="unfollow_user",
            fn_description="Unfollow a user by their FID.",
            args=[
                FunctionArgument(
                    name="target_fid",
                    description="FID of the user to unfollow.",
                    type="int",
                )
            ],
            config=FunctionConfig(
                method="delete",
                url=self.create_api_url("user/follow"),
                platform="farcaster",
                headers=self.headers,
                payload={
                    "target_fids": ["{{target_fid}}"],
                    "signer_uuid": self.signer_uuid,
                },
                success_feedback="User unfollowed successfully.",
                error_feedback="Failed to unfollow user.",
            ),
        )

    def _create_follow_channel(self) -> Function:
        """Follow Channel Function"""
        return Function(
            fn_name="follow_channel",
            fn_description="Follow a channel by its ID.",
            args=[
                FunctionArgument(
                    name="channel_id",
                    description="ID of the channel to follow.",
                    type="string",
                )
            ],
            config=FunctionConfig(
                method="post",
                url=self.create_api_url("channel/follow"),
                platform="farcaster",
                headers=self.headers,
                payload={
                    "channel_id": "{{channel_id}}",
                    "signer_uuid": self.signer_uuid,
                },
                success_feedback="Channel followed successfully.",
                error_feedback="Failed to follow channel.",
            ),
        )

    def _create_unfollow_channel(self) -> Function:
        """Unfollow Channel Function"""
        return Function(
            fn_name="unfollow_channel",
            fn_description="Unfollow a channel by its ID.",
            args=[
                FunctionArgument(
                    name="channel_id",
                    description="ID of the channel to unfollow.",
                    type="string",
                )
            ],
            config=FunctionConfig(
                method="delete",
                url=self.create_api_url("channel/follow"),
                platform="farcaster",
                headers=self.headers,
                payload={
                    "channel_id": "{{channel_id}}",
                    "signer_uuid": self.signer_uuid,
                },
                success_feedback="Channel unfollowed successfully.",
                error_feedback="Failed to unfollow channel.",
            ),
        )
