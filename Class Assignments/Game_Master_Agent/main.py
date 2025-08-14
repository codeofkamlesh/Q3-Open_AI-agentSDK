import os
import asyncio
import random
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
async def roll_dice(sides: int = 6) -> int:
    """Roll a dice with the given number of sides."""
    return random.randint(1, sides)

@function_tool
async def generate_event(context: str) -> str:
    
    events = {
        "story": [
            "You arrive at the gates of an ancient city.",
            "A mysterious traveler offers you a map.",
            "The forest whispers secrets in the wind."
        ],
        "combat": [
            "A wild goblin jumps from the bushes!",
            "A fierce dragon blocks your path!",
            "Bandits surround you with drawn swords."
        ],
        "item": [
            "You find a glowing sword in a chest.",
            "A potion shimmers on a dusty shelf.",
            "A golden key lies hidden under rubble."
        ]
    }
    return random.choice(events.get(context, ["Nothing happens..."]))



narrator_agent = Agent(
    name="NarratorAgent",
    instructions="You narrate the story progression in the fantasy adventure.",

)

monster_agent = Agent(
    name="MonsterAgent",
    instructions="You handle combat encounters, rolling dice for attack/defense.",

)

item_agent = Agent(
    name="ItemAgent",
    instructions="You handle item discoveries and inventory rewards.",

)


game_master_agent = Agent(
    name="GameMasterAgent",
    instructions=(
        "You are the Game Master of a fantasy adventure. "
        "When the user requests story progression, use NarratorAgent. "
        "When it's combat, use MonsterAgent. "
        "When it's about items, use ItemAgent. "
        "If the request is unrelated to the game, say: "
        "'I am a Game Master Agent. I run a fantasy text-based adventure game.'"
    ),
    tools=[roll_dice, generate_event]
)


async def main():
    print("\n")
    print("🎮 Welcome to Fantasy Adventure Game!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break


        next_move = await Runner.run(
            game_master_agent,
            input=user_input,
            run_config=config

        )
        print("GameMaster:", next_move.final_output)


        loot = await Runner.run(
            game_master_agent,
            input=user_input,
            run_config=config
        )



if __name__ == "__main__":
    asyncio.run(main())
