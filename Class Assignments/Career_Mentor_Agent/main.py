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

# @function_tool
# def get_career_roadmap(field: str) -> str:

#         prompt = (
#         f"You are a career skill planner. The chosen field is: {field}.\n"
#         "List the essential skills (technical and soft) needed to succeed in this field, "
#         "and suggest a short step-by-step learning plan."
#     )
#         return model.create_response(prompt)

career_agent = Agent(
    name="CareerAgent",
    instructions="You suggest suitable career fields based on the user's interests.",
    model=model
)

skill_agent = Agent(
    name="SkillAgent",
    instructions="You generate a skill roadmap for a chosen career field.",
    model=model
    # tools=[get_career_roadmap]
)

job_agent = Agent(
    name="JobAgent",
    instructions="You provide job titles and brief descriptions for a given career field.",
    model=model
)


orchestrator_agent = Agent(
    name="CareerOrchestrator",
    instructions=(
        "You are the Career Mentor Orchestrator. Your job is to decide which specialist agent should handle the request."
         "You use the tools given to you according to the given input of the user."
         "You never your own, you always use the provided tools."
         "if the user input ask anything unrelated to the agents work then show this message:"
         "I can only answer you carrer related queries"
    ),
    tools=[
        career_agent.as_tool(
            tool_name="carrer_agent",
            tool_description="suggest suitable career fields based on the user's interests.",
        ),

        # get_career_roadmap,
        skill_agent.as_tool(
            tool_name="skill_agent",
            tool_description="generate a skill roadmap for a chosen career field from carrer_agent's suggestion",
        ),

        job_agent.as_tool(
            tool_name="job_agent",
            tool_description="provide job titles and brief descriptions for a given career field",
        ),

    ]
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
