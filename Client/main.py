# # import asyncio
# # import os
# # from typing import Annotated

# # from livekit import agents, rtc
# # from livekit.agents import JobContext, WorkerOptions, cli, tokenize, tts
# # from livekit.agents.llm import ChatContext, ChatImage, ChatMessage
# # from livekit.agents.voice_assistant import VoiceAssistant
# # from livekit.plugins import deepgram, openai, silero
# # from livekit.jwt import AccessToken, VideoGrant
# # from dotenv import load_dotenv

# # # Load environment variables
# # load_dotenv()

# # # LiveKit Credentials
# # LIVEKIT_WS_URL = os.getenv("LIVEKIT_WS_URL", "wss://sinusproject-7m7ej8j7.livekit.cloud")  # Use LiveKit Cloud Playground
# # LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
# # LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

# # # Check if credentials are set
# # if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
# #     raise ValueError("Missing LIVEKIT_API_KEY or LIVEKIT_API_SECRET in environment variables.")

# # # Generate Access Token for LiveKit Agent
# # def generate_livekit_token():
# #     grant = VideoGrant(room_join=True, room="test-room")  # Replace with actual room name
# #     token = AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, grant=grant, identity="agent")
# #     return token.to_jwt()


# # class AssistantFunction(agents.llm.FunctionContext):
# #     """Defines functions that will be called by the assistant."""

# #     @agents.llm.ai_callable(
# #         description="Called when asked to analyze an image, video, or webcam feed."
# #     )
# #     async def image(self, user_msg: Annotated[str, agents.llm.TypeInfo(description="User's message triggering vision")]):
# #         print(f"🔍 Vision Triggered: {user_msg}")
# #         return None


# # async def get_video_track(room: rtc.Room):
# #     """Fetch the first available remote video track from the room."""
# #     for _, participant in room.remote_participants.items():
# #         for _, track_publication in participant.track_publications.items():
# #             if isinstance(track_publication.track, rtc.RemoteVideoTrack):
# #                 print(f"🎥 Using video track {track_publication.track.sid}")
# #                 return track_publication.track
# #     return None


# # async def entrypoint(ctx: JobContext):
# #     """Main function to connect to LiveKit and handle assistant logic."""

# #     await ctx.connect()
# #     print(f"✅ Connected to room: {ctx.room.name}")

# #     chat_context = ChatContext(
# #         messages=[
# #             ChatMessage(
# #                 role="system",
# #                 content="Your name is Alloy. You are a funny, witty AI with voice and vision. "
# #                         "Keep responses short and avoid emojis or complex punctuation."
# #             )
# #         ]
# #     )

# #     gpt = openai.LLM(model="gpt-4o")

# #     # Wrap OpenAI TTS with a Stream Adapter
# #     openai_tts = tts.StreamAdapter(
# #         tts=openai.TTS(voice="alloy"),
# #         sentence_tokenizer=tokenize.basic.SentenceTokenizer(),
# #     )

# #     latest_image: rtc.VideoFrame | None = None

# #     assistant = VoiceAssistant(
# #         vad=silero.VAD.load(),
# #         stt=deepgram.STT(),
# #         llm=gpt,
# #         tts=openai_tts,
# #         fnc_ctx=AssistantFunction(),
# #         chat_ctx=chat_context,
# #     )

# #     chat = rtc.ChatManager(ctx.room)

# #     async def _answer(text: str, use_image: bool = False):
# #         """Generate a response and optionally include the latest image."""
# #         content: list[str | ChatImage] = [text]
# #         if use_image and latest_image:
# #             content.append(ChatImage(image=latest_image))

# #         chat_context.messages.append(ChatMessage(role="user", content=content))
# #         response_stream = gpt.chat(chat_ctx=chat_context)
# #         await assistant.say(response_stream, allow_interruptions=True)

# #     @chat.on("message_received")
# #     def on_message_received(msg: rtc.ChatMessage):
# #         """Handle incoming chat messages."""
# #         if msg.message:
# #             asyncio.create_task(_answer(msg.message, use_image=False))

# #     @assistant.on("function_calls_finished")
# #     def on_function_calls_finished(called_functions: list[agents.llm.CalledFunction]):
# #         """Trigger when function calls complete."""
# #         if called_functions:
# #             user_msg = called_functions[0].call_info.arguments.get("user_msg")
# #             if user_msg:
# #                 asyncio.create_task(_answer(user_msg, use_image=True))

# #     assistant.start(ctx.room)

# #     await asyncio.sleep(1)
# #     await assistant.say("Hi there! How can I help?", allow_interruptions=True)

# #     while ctx.room.connection_state == rtc.ConnectionState.CONN_CONNECTED:
# #         video_track = await get_video_track(ctx.room)
# #         if video_track:
# #             async for event in rtc.VideoStream(video_track):
# #                 latest_image = event.frame


# # async def connect_to_livekit():
# #     """Initialize and connect to LiveKit with a token."""
# #     token = generate_livekit_token()
# #     room = rtc.Room()
# #     options = rtc.RoomOptions(auto_subscribe=True)

# #     try:
# #         await room.connect(LIVEKIT_WS_URL, token=token, options=options)
# #         print("🎉 Successfully connected to LiveKit!")
# #         return room
# #     except Exception as e:
# #         print(f"❌ Failed to connect to LiveKit: {e}")
# #         return None


# # if __name__ == "__main__":
# #     cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))


# import asyncio
# from typing import Annotated
# from dotenv import load_dotenv
# from livekit import agents, rtc
# from livekit.agents import JobContext, WorkerOptions, cli, tokenize, tts
# from livekit.agents.llm import (
#     ChatContext,
#     ChatImage,
#     ChatMessage,
# )
# from livekit.agents.voice_assistant import VoiceAssistant
# from livekit.plugins import deepgram, openai, silero
# load_dotenv()

# class AssistantFunction(agents.llm.FunctionContext):
#     """This class is used to define functions that will be called by the assistant."""

#     @agents.llm.ai_callable(
#         description=(
#             "Called when asked to evaluate something that would require vision capabilities,"
#             "for example, an image, video, or the webcam feed."
#         )
#     )
#     async def image(
#         self,
#         user_msg: Annotated[
#             str,
#             agents.llm.TypeInfo(
#                 description="The user message that triggered this function"
#             ),
#         ],
#     ):
#         print(f"Message triggering vision capabilities: {user_msg}")
#         return None


# async def get_video_track(room: rtc.Room):
#     """Get the first video track from the room. We'll use this track to process images."""

#     video_track = asyncio.Future[rtc.RemoteVideoTrack]()

#     for _, participant in room.remote_participants.items():
#         for _, track_publication in participant.track_publications.items():
#             if track_publication.track is not None and isinstance(
#                 track_publication.track, rtc.RemoteVideoTrack
#             ):
#                 video_track.set_result(track_publication.track)
#                 print(f"Using video track {track_publication.track.sid}")
#                 break

#     return await video_track


# async def entrypoint(ctx: JobContext):
#     await ctx.connect()
#     print(f"Room name: {ctx.room.name}")

#     chat_context = ChatContext(
#         messages=[
#             ChatMessage(
#                 role="system",
#                 content=(
#                     "Your name is Alloy. You are a funny, witty bot. Your interface with users will be voice and vision."
#                     "Respond with short and concise answers. Avoid using unpronouncable punctuation or emojis."
#                 ),
#             )
#         ]
#     )

#     gpt = openai.LLM(model="gpt-4o")

#     # Since OpenAI does not support streaming TTS, we'll use it with a StreamAdapter
#     # to make it compatible with the VoiceAssistant
#     openai_tts = tts.StreamAdapter(
#         tts=openai.TTS(voice="alloy"),
#         sentence_tokenizer=tokenize.basic.SentenceTokenizer(),
#     )

#     latest_image: rtc.VideoFrame | None = None

#     assistant = VoiceAssistant(
#         vad=silero.VAD.load(),  # We'll use Silero's Voice Activity Detector (VAD)
#         stt=deepgram.STT(),  # We'll use Deepgram's Speech To Text (STT)
#         llm=gpt,
#         tts=openai_tts,  # We'll use OpenAI's Text To Speech (TTS)
#         fnc_ctx=AssistantFunction(),
#         chat_ctx=chat_context,
#     )

#     chat = rtc.ChatManager(ctx.room)

#     async def _answer(text: str, use_image: bool = False):
#         """
#         Answer the user's message with the given text and optionally the latest
#         image captured from the video track.
#         """
#         content: list[str | ChatImage] = [text]
#         if use_image and latest_image:
#             content.append(ChatImage(image=latest_image))

#         chat_context.messages.append(ChatMessage(role="user", content=content))

#         stream = gpt.chat(chat_ctx=chat_context)
#         await assistant.say(stream, allow_interruptions=True)

#     @chat.on("message_received")
#     def on_message_received(msg: rtc.ChatMessage):
#         """This event triggers whenever we get a new message from the user."""

#         if msg.message:
#             asyncio.create_task(_answer(msg.message, use_image=False))

#     @assistant.on("function_calls_finished")
#     def on_function_calls_finished(called_functions: list[agents.llm.CalledFunction]):
#         """This event triggers when an assistant's function call completes."""

#         if len(called_functions) == 0:
#             return

#         user_msg = called_functions[0].call_info.arguments.get("user_msg")
#         if user_msg:
#             asyncio.create_task(_answer(user_msg, use_image=True))

#     assistant.start(ctx.room)

#     await asyncio.sleep(1)
#     await assistant.say("Hi there! How can I help?", allow_interruptions=True)

#     while ctx.room.connection_state == rtc.ConnectionState.CONN_CONNECTED:
#         video_track = await get_video_track(ctx.room)

#         async for event in rtc.VideoStream(video_track):
#             # We'll continually grab the latest image from the video track
#             # and store it in a variable.
#             latest_image = event.frame


# if __name__ == "__main__":
#     cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))


import asyncio
import os
from typing import Annotated

from dotenv import load_dotenv

from livekit import agents, rtc, api
from livekit.agents import JobContext, WorkerOptions, cli, tokenize, tts
from livekit.agents.llm import ChatContext, ChatImage, ChatMessage
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import deepgram, openai, silero

load_dotenv()

# Validate environment variables
required_vars = [
    'LIVEKIT_WS_URL',
    'LIVEKIT_API_KEY',
    'LIVEKIT_API_SECRET',
    'DEEPGRAM_API_KEY',
    'OPENAI_API_KEY'
]

for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")

print("Environment configuration:")
print(f"LiveKit URL: {os.getenv('LIVEKIT_WS_URL')}")
print(f"API Key: {os.getenv('LIVEKIT_API_KEY')[:5]}...")


class AssistantFunction(agents.llm.FunctionContext):
    @agents.llm.ai_callable(
        description="Handles vision-related requests"
    )
    async def image(
            self,
            user_msg: Annotated[
                str,
                agents.llm.TypeInfo(
                    description="User message for vision processing"
                ),
            ],
    ):
        print(f"Vision request: {user_msg}")
        return None


async def get_video_track(room: rtc.Room) -> rtc.RemoteVideoTrack:
    print("Waiting for video track...")
    while True:
        for participant in room.remote_participants.values():
            for publication in participant.track_publications.values():
                if (track := publication.track) and isinstance(track, rtc.RemoteVideoTrack):
                    print(f"Video track found: {track.sid}")
                    return track
        await asyncio.sleep(1)


async def entrypoint(ctx: JobContext):
    try:
        print("Connecting to room...")

        token = api.create_token(
            api_key=os.getenv('LIVEKIT_API_KEY'),
            api_secret=os.getenv('LIVEKIT_API_SECRET'),
            identity="ai-assistant",  # Changed identity for clarity
            name="AI Assistant",
            metadata="",
            grants={
                "room": {
                    "room": ctx.room.name or "default-room",
                    "room_join": True,
                    "can_publish": True,
                    "can_subscribe": True,
                    "can_publish_data": True
                }
            }
        )

        await ctx.connect(token=token)
        print(f"Connected to room: {ctx.room.name}")

        chat_context = ChatContext(
            messages=[
                ChatMessage(
                    role="system",
                    content="You are Alloy, a friendly AI assistant."
                ),
            ]
        )

        print("Initializing OpenAI...")
        gpt = openai.LLM(model="gpt-4")

        print("Initializing TTS...")
        tts_engine = tts.StreamAdapter(
            tts=openai.TTS(voice="alloy"),
            sentence_tokenizer=tokenize.basic.SentenceTokenizer(),
        )

        latest_image: rtc.VideoFrame | None = None

        print("Creating voice assistant...")
        assistant = VoiceAssistant(
            vad=silero.VAD.load(),
            stt=deepgram.STT(),
            llm=gpt,
            tts=tts_engine,
            fnc_ctx=AssistantFunction(),
            chat_ctx=chat_context,
        )

        chat = rtc.ChatManager(ctx.room)

        async def handle_response(text: str, use_image: bool = False):
            try:
                content = [text]
                if use_image and latest_image:
                    content.append(ChatImage(image=latest_image))
                chat_context.messages.append(ChatMessage(role="user", content=content))
                response_stream = gpt.chat(chat_ctx=chat_context)
                await assistant.say(response_stream, allow_interruptions=True)
            except Exception as e:
                print(f"Error in handle_response: {e}")

        @chat.on("message_received")
        def on_message_received(msg: rtc.ChatMessage):
            if msg.message:
                print(f"Chat message received: {msg.message}")
                asyncio.create_task(handle_response(msg.message))

        print("Starting assistant...")
        assistant.start(ctx.room)
        await assistant.say("Hello! I'm ready to help.", allow_interruptions=True)
        print("Assistant started successfully")

        while ctx.room.connection_state == rtc.ConnectionState.CONN_CONNECTED:
            try:
                video_track = await get_video_track(ctx.room)
                async for event in rtc.VideoStream(video_track):
                    latest_image = event.frame
            except Exception as e:
                print(f"Error in video processing: {e}")
                await asyncio.sleep(1)

    except Exception as e:
        print(f"Critical error: {e}")
        raise


if _name_ == "_main_":
    print("Starting LiveKit Assistant...")
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))