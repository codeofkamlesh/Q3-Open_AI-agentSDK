import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, function_tool


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


@function_tool
def get_next_move(user_action: str) -> str:
    if "cave" in user_action.lower():
        return "You find a dark tunnel. You can go left toward glowing mushrooms or right toward dripping water."
    elif "castle" in user_action.lower():
        return "A dragon blocks the main gate. You can fight, hide, or run back."
    elif "forest" in user_action.lower():
        return "You see two paths — one lit with lanterns, the other covered in fog."
    else:
        return "You wander with no clear path. Try exploring a cave, castle, or forest."


@function_tool
def generate_loot(area: str) -> str:
    if "cave" in area.lower():
        return "You find a glowing sword and 20 gold coins!"
    elif "castle" in area.lower():
        return "You discover a secret scroll of fire and a dragon scale shield!"
    elif "forest" in area.lower():
        return "You collect healing herbs and a magical bow."
    else:
        return "You find a mysterious rock that hums softly."


game_agent = Agent(
    name="GameMasterAgent",
    instructions="You are the narrator of a fantasy game. Respond to user's moves using tools to guide the story.",
    tools=[get_next_move, generate_loot]
)


async def main():
    print("🎮 Welcome to Fantasy Adventure Game!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break


        next_move = await Runner.run(
            game_agent,
            input=user_input,
            run_config=config

        )
        print("📜 GameMaster:", next_move.final_output)


        loot = await Runner.run(
            game_agent,
            input=user_input,
            run_config=config
        )
        


if __name__ == "__main__":
    asyncio.run(main())
