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

# ------------------- TOOLS -------------------
@function_tool
def get_flights(user_interest: str) -> str:
    interest = user_interest.lower()
    if "adventure" in interest:
        return "🏔️ Recommended: Thailand or Baku. Great for hiking, nature, and mountains."
    elif "relax" in interest or "beach" in interest:
        return "🏖️ Recommended: Switzerland or New York for peaceful seaside views."
    elif "budget" in interest:
        return "💸 Budget trip: Skardu or Swat — affordable and beautiful!"
    else:
        return "🤔 Please mention your travel interest (e.g., adventure, beach, budget)."

@function_tool
def suggest_hotels(destination: str) -> str:
    dest = destination.lower()
    if "thailand" in dest or "baku" in dest:
        return "🏨 Suggested Hotels: Mountain View Resort, Adventure Lodge."
    elif "switzerland" in dest or "new york" in dest:
        return "🏨 Suggested Hotels: Beach Paradise Hotel, Ocean Breeze Inn."
    elif "skardu" in dest or "swat" in dest:
        return "🏨 Suggested Hotels: Valley View Hotel, Snow Peak Inn."
    else:
        return "📦 Packing List: Travel basics - clothes, ID card, cash."

# ------------------- AGENTS -------------------
destination_agent = Agent(
    name="DestinationAgent",
    instructions="Suggest travel destinations based on mood or interests."
)

booking_agent = Agent(
    name="BookingAgent",
    instructions="Provide flight and hotel booking information."
)

explore_agent = Agent(
    name="ExploreAgent",
    instructions="Suggest attractions and food in the destination."
)

orchestrator_agent = Agent(
    name="TravelDesignerOrchestrator",
    instructions=(
        "Coordinate between agents to design a travel plan. "
        "If user asks for destinations, use DestinationAgent. "
        "If booking info, use BookingAgent. "
        "If attractions/food, use ExploreAgent. "
        "First try to use the tools. If the tools don't have related info, use the other relevant agents. "
        "If query unrelated to travel, reply: 'I am a Travel Designer Agent. "
        "I can suggest destinations, book flights/hotels, and recommend attractions.'"
    ),
    tools=[get_flights, suggest_hotels],
    handoffs=[destination_agent, booking_agent, explore_agent]
)

# ------------------- MAIN -------------------
async def main():
    print("\n")
    print("Iam AI Travel Designer Agent, Which type of trip do you like to make?")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break

        result = await Runner.run(
            orchestrator_agent,
            input=user_input,
            run_config=config
        )

        print("Agent:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
