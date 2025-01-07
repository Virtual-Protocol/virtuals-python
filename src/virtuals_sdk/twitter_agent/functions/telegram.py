from typing import Dict, List
from virtuals_sdk.twitter_agent.game import Function, FunctionConfig, FunctionArgument

class TelegramClient:
    """
    A client for managing Telegram bot functions.
    
    Initialize with your bot token to create Telegram API functions.
    
    Example:
        client = TelegramClient("your-bot-token-here")
        send_message = client.get_send_message_function()
    """
    
    def __init__(self, bot_token: str):
        """
        Initialize the Telegram client with a bot token.
        
        Args:
            bot_token (str): Your Telegram bot token
        """
        self.bot_token = bot_token

        self._functions: Dict[str, Function] = {
            "send_message": self._create_send_message(),
            "send_media": self._create_send_media(),
            "create_poll": self._create_poll(),
            "pin_message": self._create_pin_message(),
            "delete_message": self._create_delete_message(),
        }

    @property
    def available_functions(self) -> List[str]:
        """Get list of available function names."""
        return list(self._functions.keys())
    
    def create_api_url(self, endpoint):
        """Helper function to create full API URL with token"""
        return f"https://api.telegram.org/bot{self.bot_token}/{endpoint}"

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

    def _create_send_message(self) -> Function:
  
        # Send Message Function
        send_message = Function(
            fn_name="send_message",
            fn_description="Send a text message that is contextually appropriate and adds value to the conversation. Consider chat type (private/group) and ongoing discussion context.",
            args=[
                FunctionArgument(
                    name="chat_id",
                    description="Unique identifier for the target chat or username of the target channel",
                    type="string"
                ),
                FunctionArgument(
                    name="text",
                    description="Message text to send. Should be contextually relevant and maintain conversation flow.",
                    type="string"
                )
            ],
            config=FunctionConfig(
                method="post",
                url=self.create_api_url("sendMessage"),
                platform="telegram",
                headers={"Content-Type": "application/json"},
                payload={
                    "chat_id": "{{chat_id}}",
                    "text": "{{text}}",
                },
                success_feedback="Message sent successfully. Message ID: {{response.result.message_id}}",
                error_feedback="Failed to send message: {{response.description}}"
            )
        )

        return send_message


    def _create_send_media(self) -> Function:

        # Reply with Media Function
        send_media = Function(
            fn_name="send_media",
            fn_description="Send a media message (photo, document, video, etc.) with optional caption. Use when visual or document content adds value to the conversation.",
            args=[
                FunctionArgument(
                    name="chat_id",
                    description="Target chat identifier where media will be sent",
                    type="string"
                ),
                FunctionArgument(
                    name="media_type",
                    description="Type of media to send: 'photo', 'document', 'video', 'audio'. Choose appropriate type for content.",
                    type="string"
                ),
                FunctionArgument(
                    name="media",
                    description="File ID or URL of the media to send. Ensure content is appropriate and relevant.",
                    type="string"
                ),
                FunctionArgument(
                    name="caption",
                    description="Optional text caption accompanying the media. Should provide context or explanation when needed, or follows up the conversation.",
                    type="string"
                )
            ],
            config=FunctionConfig(
                method="post",
                url=self.create_api_url("send{{media_type}}"),
                platform="telegram",
                headers={"Content-Type": "application/json"},
                payload={
                    "chat_id": "{{chat_id}}",
                    "{{media_type}}": "{{media}}",
                    "caption": "{{caption}}"
                },
                success_feedback="Media sent successfully. Type: {{media_type}}, Message ID: {{response.result.message_id}}",
                error_feedback="Failed to send media: {{response.description}}"
            )
        )

        return send_media

    def _create_poll(self) -> Function:

        # Create Poll Function
        create_poll = Function(
            fn_name="create_poll",
            fn_description="Create an interactive poll to gather user opinions or make group decisions. Useful for engagement and collecting feedback.",
            args=[
                FunctionArgument(
                    name="chat_id",
                    description="Chat where the poll will be created",
                    type="string"
                ),
                FunctionArgument(
                    name="question",
                    description="Main poll question. Should be clear and specific.",
                    type="string"
                ),
                FunctionArgument(
                    name="options",
                    description="List of answer options. Make options clear and mutually exclusive.",
                    type="array"
                ),
                FunctionArgument(
                    name="is_anonymous",
                    description="Whether poll responses are anonymous. Consider privacy and group dynamics.",
                    type="boolean"
                )
            ],
            config=FunctionConfig(
                method="post",
                url=self.create_api_url("sendPoll"),
                platform="telegram",
                headers={"Content-Type": "application/json"},
                payload={
                    "chat_id": "{{chat_id}}",
                    "question": "{{question}}",
                    "options": "{{options}}",
                    "is_anonymous": "{{is_anonymous}}",
                },
                success_feedback="Poll created successfully. Poll ID: {{response.result.poll.id}}",
                error_feedback="Failed to create poll: {{response.description}}"
            )
        )

        return create_poll
    
    def _create_pin_message(self) -> Function:

        # Pin Message Function
        pin_message = Function(
            fn_name="pin_message",
            fn_description="Pin an important message in a chat. Use for announcements, important information, or group rules.",
            args=[
                FunctionArgument(
                    name="chat_id",
                    description="Chat where the message will be pinned",
                    type="string"
                ),
                FunctionArgument(
                    name="message_id",
                    description="ID of the message to pin. Ensure message contains valuable information worth pinning.",
                    type="string"
                ),
                FunctionArgument(
                    name="disable_notification",
                    description="Whether to send notification about pinned message. Consider group size and message importance.",
                    type="boolean"
                )
            ],
            config=FunctionConfig(
                method="post",
                url=self.create_api_url("pinChatMessage"),
                platform="telegram",
                headers={"Content-Type": "application/json"},
                payload={
                    "chat_id": "{{chat_id}}",
                    "message_id": "{{message_id}}",
                    "disable_notification": "{{disable_notification}}"
                },
                success_feedback="Message pinned successfully",
                error_feedback="Failed to pin message: {{response.description}}"
            )
        )

        return pin_message

    def _create_delete_message(self) -> Function:

        # Delete Message Function
        delete_message = Function(
            fn_name="delete_message",
            fn_description="Delete a message from a chat. Use for moderation or cleaning up outdated information.",
            args=[
                FunctionArgument(
                    name="chat_id",
                    description="Chat containing the message to delete",
                    type="string"
                ),
                FunctionArgument(
                    name="message_id",
                    description="ID of the message to delete. Consider impact before deletion.",
                    type="string"
                )
            ],
            config=FunctionConfig(
                method="post",
                url=self.create_api_url("deleteMessage"),
                platform="telegram",
                headers={"Content-Type": "application/json"},
                payload={
                    "chat_id": "{{chat_id}}",
                    "message_id": "{{message_id}}"
                },
                success_feedback="Message deleted successfully",
                error_feedback="Failed to delete message: {{response.description}}"
            )
        )

        return delete_message


    ## FAILS BECAUSE CHATS ARE USUALLY PRIVATE AND AGENTS (BOT TOKEN) CANNOT CHANGE PRIVATE CHAT TITLES
    # def _create_set_chat_title(self) -> Function:
    #     # Set Chat Title Function
    #     set_chat_title = Function(
    #         fn_name="set_chat_title",
    #         fn_description="Update the title of a group, supergroup, or channel. Use when title needs updating to reflect current purpose.",
    #         args=[
    #             FunctionArgument(
    #                 name="chat_id",
    #                 description="Chat identifier where title will be updated",
    #                 type="string"
    #             ),
    #             FunctionArgument(
    #                 name="title",
    #                 description="New chat title. Should be descriptive and appropriate for chat purpose.",
    #                 type="string"
    #             )
    #         ],
    #         config=FunctionConfig(
    #             method="post",
    #             url=self.create_api_url("setChatTitle"),
    #             platform="telegram",
    #             headers={"Content-Type": "application/json"},
    #             payload={
    #                 "chat_id": "{{chat_id}}",
    #                 "title": "{{title}}"
    #             },
    #             success_feedback="Chat title updated successfully",
    #             error_feedback="Failed to update chat title: {{response.description}}"
    #         )
    #     )

    #     return set_chat_title