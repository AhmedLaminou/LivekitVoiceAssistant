# agent_runner.py
import os
import asyncio
import httpx
from dotenv import load_dotenv

# LiveKit agents (v1.x) APIs
from livekit import rtc
from livekit.agents import AgentSession, Agent, RoomInputOptions, AutoSubscribe

# tools
from tools import turn_on_light, turn_off_light, get_light_status

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

# simple LLM caller via OpenRouter (chat completions)
async def ask_llm(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a helpful smart-home assistant. If the user asks to run a tool, respond with JSON: {\"tool\": \"tool_name\", \"args\": {...}}. Otherwise respond normally."},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]

# helper: parse simple tool-calling JSON returned by the LLM
import json
def try_parse_tool_call(llm_text: str):
    """
    Expect LLM to return JSON like:
      {"tool": "turn_on_light", "args": {"room": "KITCHEN"}}
    If not present, return None.
    """
    try:
        payload = json.loads(llm_text)
        if isinstance(payload, dict) and "tool" in payload:
            return payload
    except Exception:
        return None
    return None

async def run_agent(livekit_url: str, token: str):
    """
    This uses AgentSession (v1.x) to attach an agent to a room.
    It:
      - connects an rtc.Room to LiveKit
      - creates an AgentSession and starts it, which wires STT/TTS
      - listens for final user transcriptions and responds via the LLM
      - if LLM returns a tool-call JSON, execute the tool and speak its result
    Notes:
      - RoomInputOptions / AutoSubscribe allow setting auto_subscribe behavior.
      - Depending on which plugins you installed (noise cancellation, stt providers),
        some RoomInputOptions fields may vary.
    References: LiveKit Agents docs (AgentSession, Agent, RoomInputOptions). 
    """
    room = rtc.Room()
    await room.connect(livekit_url, token)

    # create an AgentSession (orchestrator) instance
    session = AgentSession()

    # create a basic Agent with instructions
    my_agent = Agent(instructions="You are a concise smart-home assistant. For explicit tool calls, reply with a JSON object {'tool': 'name', 'args': {...}}.")

    # choose room input options: audio-only auto-subscribe
    rio = RoomInputOptions(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # start the session attached to the connected room
    await session.start(room=room, agent=my_agent, room_input_options=rio)

    # subscribe to session-level transcription events
    # the exact event name or callback signature can vary; the SDK exposes an event emitter.
    # We'll use session.on('transcription', handler) style — if your installed SDK differs,
    # adapt the handler registration per docs.
    def make_handler(sess):
        async def _on_transcript(evt):
            # evt likely has attributes: text, is_final, participant
            text = getattr(evt, "text", None) or getattr(evt, "transcript", None)
            is_final = getattr(evt, "is_final", getattr(evt, "final", True))
            if not text or not is_final:
                return
            print("User said:", text)

            # ask LLM
            llm_reply = await ask_llm(text)
            print("LLM reply:", llm_reply)

            # attempt to parse tool call
            tool_call = try_parse_tool_call(llm_reply)
            if tool_call:
                tool = tool_call.get("tool")
                args = tool_call.get("args", {})
                try:
                    if tool == "turn_on_light":
                        res = turn_on_light(args.get("room"))
                    elif tool == "turn_off_light":
                        res = turn_off_light(args.get("room"))
                    elif tool == "get_light_status":
                        res = get_light_status(args.get("room"))
                    else:
                        res = f"Unknown tool: {tool}"
                except Exception as e:
                    res = f"Tool error: {e}"
                # speak the tool result via session TTS
                await session.speak(res)
            else:
                # no tool call — speak the LLM's reply directly
                await session.speak(llm_reply)
        return _on_transcript

    # register handler
    session.on("transcription", make_handler(session))

    print("AgentSession started and listening in room:", room.sid if hasattr(room, "sid") else "unknown")

    # keep alive until room closes
    await session.wait_closed()
