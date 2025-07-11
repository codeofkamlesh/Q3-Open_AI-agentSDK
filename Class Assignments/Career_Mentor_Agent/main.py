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
def get_career_roadmap(career_name: str) -> str:
    roadmap = {
        "software developer": ["Python", "Git", "APIs"],
        "marketing manager": ["Communication", "SEO", "Data Analysis"],
        "graphic designer": ["Photoshop", "Illustrator", "Creativity"]
    }
    name = career_name.lower()
    if name in roadmap:
        skills = roadmap[name]
        return f"{career_name.title()} banne ke liye yeh skills chahiye: {', '.join(skills)}"
    else:
        return f"Sorry, roadmap nahi mili '{career_name.title()}' ke liye."

@function_tool
def get_job_roles(career_name: str) -> str:
    jobs = {
        "software developer": ["Junior Developer", "Backend Engineer"],
        "marketing manager": ["SEO Specialist", "Brand Manager"],
        "graphic designer": ["Logo Designer", "UI Designer"]
    }
    name = career_name.lower()
    if name in jobs:
        roles = jobs[name]
        return f"{career_name.title()} ke liye yeh job roles mil sakte hain: {', '.join(roles)}"
    else:
        return f"Sorry, job roles nahi mile '{career_name.title()}' ke liye."


career_agent = Agent(
    name="CareerAgent",
    instructions="User se interest lo aur career options suggest karo."
)

skill_agent = Agent(
    name="SkillAgent",
    instructions="Career name mile to get_career_roadmap tool se skills do."
)

job_agent = Agent(
    name="JobAgent",
    instructions="Career name mile to get_job_roles tool se job titles do."
)


interest_map = {
    "technology": ["Software Developer", "AI Engineer"],
    "business": ["Marketing Manager", "Business Analyst"],
    "design": ["Graphic Designer", "UI/UX Designer"]
}

def get_career_from_interest(text: str):
    for interest, careers in interest_map.items():
        if interest in text.lower():
            return f"Aap ke liye career options hain: {', '.join(careers)}"
    return None


async def main():
    print("🎓 Career Mentor Agent (CLI Version)")
    print("Type 'exit' to quit.\n")
    print("In which field you want to make your career? ")
    while True:
        user_input = input("You: ").strip().lower()
        if user_input == "exit":
            break

        # Step 1: Suggest careers from interest
        career_suggestion = get_career_from_interest(user_input)
        if career_suggestion:
            print("CareerAgent:", career_suggestion)
            continue

        # Step 2: Handoff if user types known career
        all_careers = ["software developer", "marketing manager", "graphic designer"]
        if user_input in all_careers:
            # SkillAgent
            skills = await Runner.run(
                skill_agent,
                input=user_input,
                run_config=config,
                tools=[get_career_roadmap]
            )
            print("SkillAgent:", skills.final_output)

            # JobAgent
            jobs = await Runner.run(
                job_agent,
                input=user_input,
                run_config=config,
                tools=[get_job_roles]
            )
            print("JobAgent:", jobs.final_output)
            continue

        # Step 3: Fallback (CareerAgent via LLM)
        fallback = await Runner.run(
            career_agent,
            input=user_input,
            run_config=config
        )
        print("CareerAgent:", fallback.final_output)


if __name__ == "__main__":
    asyncio.run(main())
