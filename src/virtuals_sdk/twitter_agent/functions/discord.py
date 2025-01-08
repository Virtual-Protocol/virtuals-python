from typing import Dict, List
from virtuals_sdk.twitter_agent.game import Function, FunctionConfig, FunctionArgument


class DiscordClient:
    """
    A client for managing Discord bot functions.

    Initialize with your bot token to create Discord API functions.

    Example:
        client = DiscordClient("your-bot-token-here")
        send_message = client.get_function("send_message")
    """

    def __init__(self, bot_token: str):
        """
        Initialize the Discord client with a bot token.

        Args:
            bot_token (str): Your Discord bot token
        """
        self.bot_token = bot_token

        self._functions: Dict[str, Function] = {
            "send_message": self._create_send_message(),
            "add_reaction": self._create_add_reaction(),
            "pin_message": self._create_pin_message(),
            "delete_message": self._create_delete_message(),
        }

    @property
    def available_functions(self) -> List[str]:
        """Get list of available function names."""
        return list(self._functions.keys())

    def create_api_url(self, endpoint: str) -> str:
        """Helper function to create full API URL with token"""
        return f"https://discord.com/api/v10/{endpoint}"

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

    def _create_send_message(self) -> Function:

        # Send Message Function
        send_message = Function(
            fn_name="send_message",
            fn_description="Send a text message to a Discord channel.",
            args=[
                FunctionArgument(
                    name="channel_id",
                    description="ID of the Discord channel to send the message to.",
                    type="string",
                ),
                FunctionArgument(
                    name="content",
                    description="Content of the message to send.",
                    type="string",
                ),
            ],
            config=FunctionConfig(
                method="post",
                url=self.create_api_url("channels/{{channel_id}}/messages"),
                platform="discord",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bot {self.bot_token}",
                },
                payload={
                    "content": "{{content}}",
                },
                success_feedback="Message sent successfully.",
                error_feedback="Failed to send message: {{response.message}}",
            ),
        )

        return send_message

    def _create_add_reaction(self) -> Function:

        # Add Reaction Function
        add_reaction = Function(
            fn_name="add_reaction",
            fn_description="Add a reaction emoji to a message.",
            args=[
                FunctionArgument(
                    name="channel_id",
                    description="ID of the Discord channel containing the message.",
                    type="string",
                ),
                FunctionArgument(
                    name="message_id",
                    description="ID of the message to add a reaction to.",
                    type="string",
                ),
                FunctionArgument(
                    name="emoji",
                    description="Emoji to add as a reaction (Unicode or custom emoji).",
                    type="string",
                ),
            ],
            config=FunctionConfig(
                method="put",
                url=self.create_api_url(
                    "channels/{{channel_id}}/messages/{{message_id}}/reactions/{{emoji}}/@me"
                ),
                platform="discord",
                headers={"Authorization": f"Bot {self.bot_token}"},
                success_feedback="Reaction added successfully.",
                error_feedback="Failed to add reaction: {{response.message}}",
            ),
        )

        return add_reaction

    def _create_pin_message(self) -> Function:

        # Pin Message Function
        pin_message = Function(
            fn_name="pin_message",
            fn_description="Pin a message in a Discord channel.",
            args=[
                FunctionArgument(
                    name="channel_id",
                    description="ID of the Discord channel containing the message.",
                    type="string",
                ),
                FunctionArgument(
                    name="message_id",
                    description="ID of the message to pin.",
                    type="string",
                ),
            ],
            config=FunctionConfig(
                method="put",
                url=self.create_api_url("channels/{{channel_id}}/pins/{{message_id}}"),
                platform="discord",
                headers={"Authorization": f"Bot {self.bot_token}"},
                success_feedback="Message pinned successfully.",
                error_feedback="Failed to pin message: {{response.message}}",
            ),
        )

        return pin_message

    def _create_delete_message(self) -> Function:

        # Delete Message Function
        delete_message = Function(
            fn_name="delete_message",
            fn_description="Delete a message from a Discord channel.",
            args=[
                FunctionArgument(
                    name="channel_id",
                    description="ID of the Discord channel containing the message.",
                    type="string",
                ),
                FunctionArgument(
                    name="message_id",
                    description="ID of the message to delete.",
                    type="string",
                ),
            ],
            config=FunctionConfig(
                method="delete",
                url=self.create_api_url(
                    "channels/{{channel_id}}/messages/{{message_id}}"
                ),
                platform="discord",
                headers={"Authorization": f"Bot {self.bot_token}"},
                success_feedback="Message deleted successfully.",
                error_feedback="Failed to delete message: {{response.message}}",
            ),
        )

        return delete_message
