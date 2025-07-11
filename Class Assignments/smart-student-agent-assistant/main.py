from agents import Agent,  Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig

import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

model = OpenAIChatCompletionsModel(
model = "gemini-2.0-flash",
openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True

)

agent = Agent(
 name="Smart-Student-Agent-Assistant",
 instructions="you are a student Agent you will provide information only about study related material and education",

)

result= Runner.run_sync(
    agent,
    input = "Hellow how may i help you",
    run_config=config
)

print(result.final_output)