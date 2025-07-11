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
def get_travel_plan(user_interest: str) -> str:
    interest = user_interest.lower()
    if "adventure" in interest:
        return "🏔️ Recommended: Skardu or Hunza. Great for hiking, nature, and mountains."
    elif "relax" in interest or "beach" in interest:
        return "🏖️ Recommended: Gwadar or Clifton Beach for peaceful seaside views."
    elif "budget" in interest:
        return "💸 Budget trip: Visit Murree or Swat — affordable and beautiful!"
    else:
        return "🤔 Please mention your travel interest (e.g., adventure, beach, budget)."


@function_tool
def get_packing_list(destination: str) -> str:
    dest = destination.lower()
    if "skardu" in dest or "hunza" in dest:
        return "🧳 Packing List: Jacket, hiking boots, sunglasses, water bottle."
    elif "beach" in dest or "gwadar" in dest:
        return "🧳 Packing List: Sunscreen, hat, swimwear, flip-flops."
    elif "murree" in dest or "swat" in dest:
        return "🧳 Packing List: Warm clothes, camera, snacks."
    else:
        return "📦 Packing List: Travel basics - clothes, ID card, cash."


travel_agent = Agent(
    name="TravelAgent",
    instructions="You are a Travel Designer. Based on user's interest or budget, suggest travel plans and packing list.",
    tools=[get_travel_plan, get_packing_list]
)


async def main():
    print("🧭 AI Travel Designer (CLI Version)")
    print("Type 'exit' to quit.\n")
    print("For which place would you like to make a trip?")
    while True:
        user_input = input("You: ").strip().lower()
        if user_input == "exit":
            break


        if "travel" in user_input or "trip" in user_input or "adventure" in user_input or "budget" in user_input:
            plan = await Runner.run(
                travel_agent,
                input=user_input,
                run_config=config,

            )
            print("🗺️ Travel Suggestion:", plan.final_output)
            continue


        destinations = ["skardu", "hunza", "gwadar", "beach", "murree", "swat"]
        if any(dest in user_input for dest in destinations):
            packing = await Runner.run(
                travel_agent,
                input=user_input,
                run_config=config,

            )
            print("🎒 Packing List:", packing.final_output)
            continue


        fallback = await Runner.run(
            travel_agent,
            input=user_input,
            run_config=config
        )
        print("🤖 TravelAgent:", fallback.final_output)


if __name__ == "__main__":
    asyncio.run(main())
