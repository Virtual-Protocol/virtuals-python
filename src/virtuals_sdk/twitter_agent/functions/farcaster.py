from typing import Dict, List
from virtuals_sdk.twitter_agent.game import Function, FunctionConfig, FunctionArgument

class FarcasterClient:
    """
    A client for managing Farcaster social interactions using Neynar API.
    Each function is designed with simple, intuitive arguments for LLM agents.
    """
    
    def __init__(self, api_key: str, signer_uuid: str):
        """
        Initialize the Farcaster client.
        
        Args:
            api_key (str): Your Neynar API key
            signer_uuid (str): Default signer UUID for all operations
        """
        self.api_key = api_key
        self.signer_uuid = signer_uuid
        self.base_url = "https://api.neynar.com/v2"
        self.base_headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api_key": self.api_key
        }

        self._functions: Dict[str, Function] = {
            # Content Creation
            "post_cast": self._create_post_cast(),
            "reply_to_cast": self._create_reply_to_cast(),
            
            # Engagement Actions
            "recast": self._create_recast(),
            "like_cast": self._create_like_cast(),
            "unlike_cast": self._create_unlike_cast(),
            
            # Channel Operations
            "create_channel": self._create_channel(),
            "post_to_channel": self._create_post_to_channel(),
            
            # Feed Retrieval
            "get_trending_casts": self._create_get_trending_casts(),
            "get_user_casts": self._create_get_user_casts(),
            "get_cast_reactions": self._create_get_cast_reactions(),
            
            # Search Functions
            "search_casts": self._create_search_casts(),
            "search_users": self._create_search_users(),
        }

    @property
    def available_functions(self) -> List[str]:
        """Get list of available function names."""
        return list(self._functions.keys())

    def get_function(self, fn_name: str) -> Function:
        """Get a specific function by name."""
        if fn_name not in self._functions:
            raise ValueError(f"Function '{fn_name}' not found. Available functions: {', '.join(self.available_functions)}")
        return self._functions[fn_name]

    def _create_post_cast(self) -> Function:
        return Function(
            fn_name="post_cast",
            fn_description="Create a new cast (post) on Farcaster. Use this to share thoughts, insights, or start new discussions.",
            args=[
                FunctionArgument(
                    name="text",
                    description="The content of your cast. Should be engaging and contextual. Max 320 characters.",
                    type="string"
                ),
                FunctionArgument(
                    name="embed_url",
                    description="Optional URL to embed in the cast (e.g., link to an article, image, or video)",
                    type="string",
                    required=False
                )
            ],
            config=FunctionConfig(
                method="post",
                url=f"{self.base_url}/farcaster/cast",
                platform="farcaster",
                headers=self.base_headers,
                payload={
                    "signer_uuid": self.signer_uuid,
                    "text": "{{text}}",
                    "embeds": [{"url": "{{embed_url}}"}] if "{{embed_url}}" else []
                },
                success_feedback="Cast posted successfully. Preview: '{{response.cast.text}}' {{#response.cast.embeds.[0]}}with embedded content from {{response.cast.embeds.[0].url}}{{/response.cast.embeds.[0]}}"
            )
        )

    def _create_reply_to_cast(self) -> Function:
        return Function(
            fn_name="reply_to_cast",
            fn_description="Reply to an existing cast. Use this to engage in conversations or provide feedback to others.",
            args=[
                FunctionArgument(
                    name="text",
                    description="Your reply message. Should be relevant to the conversation. Max 320 characters.",
                    type="string"
                ),
                FunctionArgument(
                    name="cast_hash",
                    description="The hash of the cast you're replying to",
                    type="string"
                )
            ],
            config=FunctionConfig(
                method="post",
                url=f"{self.base_url}/farcaster/cast",
                platform="farcaster",
                headers=self.base_headers,
                payload={
                    "signer_uuid": self.signer_uuid,
                    "text": "{{text}}",
                    "parent": "{{cast_hash}}"
                },
                success_feedback="Reply posted successfully. Your reply: '{{response.cast.text}}' to cast by {{response.cast.parent_author.username}}"
            )
        )

    def _create_recast(self) -> Function:
        return Function(
            fn_name="recast",
            fn_description="Share another user's cast with your followers. Use this to amplify valuable content.",
            args=[
                FunctionArgument(
                    name="cast_hash",
                    description="Hash of the cast you want to share with your followers",
                    type="string"
                )
            ],
            config=FunctionConfig(
                method="post",
                url=f"{self.base_url}/farcaster/recast",
                platform="farcaster",
                headers=self.base_headers,
                payload={
                    "signer_uuid": self.signer_uuid,
                    "target_hash": "{{cast_hash}}"
                },
                success_feedback="Successfully shared cast by {{response.cast.author.username}}. Original cast: '{{response.cast.text}}'"
            )
        )

    def _create_like_cast(self) -> Function:
        return Function(
            fn_name="like_cast",
            fn_description="Like a cast to show appreciation or agreement.",
            args=[
                FunctionArgument(
                    name="cast_hash",
                    description="Hash of the cast you want to like",
                    type="string"
                )
            ],
            config=FunctionConfig(
                method="post",
                url=f"{self.base_url}/farcaster/reaction",
                platform="farcaster",
                headers=self.base_headers,
                payload={
                    "signer_uuid": self.signer_uuid,
                    "target_hash": "{{cast_hash}}",
                    "reaction_type": "like"
                },
                success_feedback="Liked cast by {{response.cast.author.username}}. Cast text: '{{response.cast.text}}'"
            )
        )

    def _create_unlike_cast(self) -> Function:
        return Function(
            fn_name="unlike_cast",
            fn_description="Remove your like from a cast.",
            args=[
                FunctionArgument(
                    name="cast_hash",
                    description="Hash of the cast to unlike",
                    type="string"
                )
            ],
            config=FunctionConfig(
                method="delete",
                url=f"{self.base_url}/farcaster/reaction",
                platform="farcaster",
                headers=self.base_headers,
                payload={
                    "signer_uuid": self.signer_uuid,
                    "target_hash": "{{cast_hash}}",
                    "reaction_type": "like"
                },
                success_feedback="Removed like from cast by {{response.cast.author.username}}"
            )
        )

    def _create_channel(self) -> Function:
        return Function(
            fn_name="create_channel",
            fn_description="Create a new channel on Farcaster. Use this to start a focused discussion space.",
            args=[
                FunctionArgument(
                    name="name",
                    description="Name of the channel (without leading 'fc:')",
                    type="string"
                ),
                FunctionArgument(
                    name="description",
                    description="Short description of what the channel is about",
                    type="string"
                )
            ],
            config=FunctionConfig(
                method="post",
                url=f"{self.base_url}/farcaster/channel",
                platform="farcaster",
                headers=self.base_headers,
                payload={
                    "name": "{{name}}",
                    "description": "{{description}}"
                },
                success_feedback="Channel 'fc:{{response.channel.name}}' created successfully. Description: {{response.channel.description}}"
            )
        )

    def _create_post_to_channel(self) -> Function:
        return Function(
            fn_name="post_to_channel",
            fn_description="Post a cast to a specific channel. Use this to participate in topic-specific discussions.",
            args=[
                FunctionArgument(
                    name="text",
                    description="The content of your cast. Should be relevant to the channel topic. Max 320 characters.",
                    type="string"
                ),
                FunctionArgument(
                    name="channel_name",
                    description="Name of the channel to post to (without leading 'fc:')",
                    type="string"
                )
            ],
            config=FunctionConfig(
                method="post",
                url=f"{self.base_url}/farcaster/cast",
                platform="farcaster",
                headers=self.base_headers,
                payload={
                    "signer_uuid": self.signer_uuid,
                    "text": "{{text}}",
                    "channel": "{{channel_name}}"
                },
                success_feedback="Posted to channel fc:{{response.cast.channel}}: '{{response.cast.text}}'"
            )
        )

    def _create_get_trending_casts(self) -> Function:
        return Function(
            fn_name="get_trending_casts",
            fn_description="Get currently trending casts on Farcaster. Use this to understand current discussions and hot topics.",
            args=[
                FunctionArgument(
                    name="time_window",
                    description="Time window for trending casts: '1h', '6h', '24h', or '7d'",
                    type="string",
                    required=False
                )
            ],
            config=FunctionConfig(
                method="get",
                url=f"{self.base_url}/farcaster/feed/trending",
                platform="farcaster",
                headers=self.base_headers,
                query_params={
                    "time_window": "{{time_window}}"
                },
                success_feedback="Found {{response.casts.length}} trending casts. Top 3 trending: 1) '{{response.casts.[0].text}}' by {{response.casts.[0].author.username}} ({{response.casts.[0].reactions.likes}} likes), 2) '{{response.casts.[1].text}}' ({{response.casts.[1].reactions.likes}} likes), 3) '{{response.casts.[2].text}}' ({{response.casts.[2].reactions.likes}} likes)"
            )
        )

    def _create_get_cast_reactions(self) -> Function:
        return Function(
            fn_name="get_cast_reactions",
            fn_description="Get reactions (likes, recasts) for a specific cast. Use this to gauge a cast's impact.",
            args=[
                FunctionArgument(
                    name="cast_hash",
                    description="Hash of the cast to get reactions for",
                    type="string"
                )
            ],
            config=FunctionConfig(
                method="get",
                url=f"{self.base_url}/farcaster/cast/{{cast_hash}}/reactions",
                platform="farcaster",
                headers=self.base_headers,
                success_feedback="Cast has {{response.reactions.likes}} likes and {{response.reactions.recasts}} recasts. Top engaging users: {{response.reactions.top_likers.[0].username}}, {{response.reactions.top_likers.[1].username}}, {{response.reactions.top_likers.[2].username}}"
            )
        )

    def _create_get_user_casts(self) -> Function:
        return Function(
            fn_name="get_user_casts",
            fn_description="Get recent casts from a specific user. Use this to understand a user's activity and interests.",
            args=[
                FunctionArgument(
                    name="fid",
                    description="Farcaster ID of the user",
                    type="integer"
                )
            ],
            config=FunctionConfig(
                method="get",
                url=f"{self.base_url}/farcaster/user/casts",
                platform="farcaster",
                headers=self.base_headers,
                query_params={
                    "fid": "{{fid}}"
                },
                success_feedback="Retrieved {{response.casts.length}} casts by {{response.casts.[0].author.username}}. Latest: '{{response.casts.[0].text}}' ({{response.casts.[0].reactions.likes}} likes). Most engaged: '{{response.most_liked_cast.text}}' ({{response.most_liked_cast.reactions.likes}} likes)"
            )
        )

    def _create_search_casts(self) -> Function:
        return Function(
            fn_name="search_casts",
            fn_description="Search for casts containing specific text or topics.",
            args=[
                FunctionArgument(
                    name="query",
                    description="Text to search for in casts",
                    type="string"
                ),
                FunctionArgument(
                    name="channel_name",
                    description="Optional: Filter search to a specific channel",
                    type="string",
                    required=False
                )
            ],
            config=FunctionConfig(
                method="get",
                url=f"{self.base_url}/farcaster/cast/search",
                platform="farcaster",
                headers=self.base_headers,
                query_params={
                    "q": "{{query}}",
                    "channel": "{{channel_name}}"
                },
                success_feedback="Found {{response.casts.length}} matching casts. Most relevant: 1) '{{response.casts.[0].text}}' by {{response.casts.[0].author.username}} in channel {{response.casts.[0].channel}} ({{response.casts.[0].reactions.likes}} likes), 2) '{{response.casts.[1].text}}' ({{response.casts.[1].reactions.likes}} likes)"
            )
        )

    def _create_search_users(self) -> Function:
        return Function(
            fn_name="search_users",
            fn_description="Search for Farcaster users by username or display name.",
            args=[
                FunctionArgument(
                    name="query",
                    description="Text to search for in usernames or display names",
                    type="string"
                )
            ],
            config=FunctionConfig(
                method="get",
                url=f"{self.base_url}/farcaster/user/search",
                platform="farcaster",
                headers=self.base_headers,
                query_params={
                    "q": "{{query}}"
                },
                success_feedback="Found {{response.users.length}} users. Top matches: {{response.users.[0].username}} ({{response.users.[0].display_name}}), {{response.users.[1].username}} ({{response.users.[1].display_name}})",
                error_feedback="Failed to search users: {{response.message}}"
            )
        )

    def _create_get_user_casts(self) -> Function:
        return Function(
            fn_name="get_user_casts",
            fn_description="Get recent casts from a specific user. Use this to understand a user's activity and interests.",
            args=[
                FunctionArgument(
                    name="fid",
                    description="Farcaster ID of the user",
                    type="integer"
                )
            ],
            config=FunctionConfig(
                method="get",
                url=f"{self.base_url}/farcaster/user/casts",
                platform="farcaster",
                headers=self.base_headers,
                query_params={
                    "fid": "{{fid}}"
                },
                success_feedback="Retrieved {{response.casts.length}} recent casts. Latest cast: '{{response.casts.[0].text}}' with {{response.casts.[0].reactions.likes}} likes. Most liked cast: '{{response.most_liked_cast.text}}' with {{response.most_liked_cast.reactions.likes}} likes",
                error_feedback="Failed to get user's casts: {{response.message}}"
            )
        )

    def _create_get_cast_reactions(self) -> Function:
        return Function(
            fn_name="get_cast_reactions",
            fn_description="Get reactions (likes, recasts) for a specific cast. Use this to gauge a cast's impact.",
            args=[
                FunctionArgument(
                    name="cast_hash",
                    description="Hash of the cast to get reactions for",
                    type="string"
                )
            ],
            config=FunctionConfig(
                method="get",
                url=f"{self.base_url}/farcaster/cast/{{cast_hash}}/reactions",
                platform="farcaster",
                headers=self.base_headers,
                success_feedback="Cast has {{response.reactions.likes}} likes and {{response.reactions.recasts}} recasts. Most engaged users: {{response.reactions.top_likers.[0].username}}, {{response.reactions.top_likers.[1].username}}",
                error_feedback="Failed to get cast reactions: {{response.message}}"
            )
        )