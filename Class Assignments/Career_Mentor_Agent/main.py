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
def get_career_roadmap(field: str) -> str:

        roadmaps = {
        "graphic designing": "start with photoshop, illustrator, canva.",
        "web development": "you should first start with HTML, CSS, JAVASCRIPT, then React.js or Next.js.",
        "Video Editing":"you should satrt with Filmora, premier pro , then after effect for Animation."
        }
        return roadmaps.get(field.lower(), f"No roadmap available for {field}.")

career_agent = Agent(
    name="CareerAgent",
    instructions="You suggest suitable career fields based on the user's interests.",
    model=model
)

skill_agent = Agent(
    name="SkillAgent",
    instructions="You generate a skill roadmap for a chosen career field.",
    model=model

)

job_agent = Agent(
    name="JobAgent",
    instructions="You provide job titles and brief descriptions for a given career field.",
    model=model
)


orchestrator_agent = Agent(
    name="CareerOrchestrator",
    instructions=(
        "You are the Career Mentor Orchestrator. Your job is to handoff the task to specialist agent should handle the request."
         "You use the tools given to you according to the given input of the user."
         "if user is asking about the roadmap of field other than mentioned in tool then take resuls from the model."
         "if the user input ask anything unrelated to the agents work then show this message:"
         "I can only answer you carrer related queries"
    ),
    tools=[get_career_roadmap],
   

)


async def main():
    print("\n")
    print("Hi ! Iam a Career Mentor Agent")
    print("\n")
    print("In which field would you like make your carrer, tell me your interest first?")
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

        print("Output:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
