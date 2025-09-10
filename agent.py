import asyncio
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import google, noise_cancellation
from Cosmo_prompts import behavior_prompts, Reply_prompts
from Cosmo_google_search import google_search, get_current_datetime
from Cosmo_get_whether import get_weather
from Cosmo_window_CTRL import open, close, folder_file
from Cosmo_file_opner import Play_file
from Cosmo_kb_mouse_CTRL import (
    move_cursor_tool, mouse_click_tool, scroll_cursor_tool,
    type_text_tool, press_key_tool, swipe_gesture_tool,
    press_hotkey_tool, control_volume_tool
)

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=behavior_prompts,
                         tools=[
                             google_search,
                             get_current_datetime,
                             get_weather,
                             open,
                             close,
                             folder_file,
                             Play_file,
                             move_cursor_tool,
                             mouse_click_tool,
                             scroll_cursor_tool,
                             type_text_tool,
                             press_key_tool,
                             press_hotkey_tool,
                             control_volume_tool,
                             swipe_gesture_tool
                         ]
                         )

    async def on_user_message(self, message: str):
        # Check for shutdown command
        if message.strip().lower() in ["shutdown", "quit", "exit", "close cosmo"]:
            await self.shutdown()
            return "OK Boss, I am closing the system..."
        return None


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            voice="Charon"
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
            video_enabled=True
        ),
    )

    await ctx.connect()

    # Generate replies continuously
    while True:
        reply = await session.generate_reply(
            instructions=Reply_prompts
        )
        # Optional: stop loop if assistant shutdown
        if reply.lower().startswith("ok boss, i am closing"):
            await session.end()
            break


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
