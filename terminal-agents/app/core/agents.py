from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, OpenAIResponsesModel, Runner, RawResponsesStreamEvent, AgentUpdatedStreamEvent, RunItemStreamEvent
from app.config.settings import OPENAI_API_KEY
from app.core.prompts import CURRENT_SYSTEM_PROMPT
from app.config.utils import logger


openai_gpt4_mini = OpenAIResponsesModel(
    model="gpt-4.1-mini",
    openai_client=AsyncOpenAI(api_key=OPENAI_API_KEY),
)

shopping_agent = Agent(
    name="Shopping Agent",
    instructions=CURRENT_SYSTEM_PROMPT,
    model=openai_gpt4_mini,
    # tools=get_tool_definitions()
)

generic_agent = Agent(
    name="Generic Agent",
    instructions="You are a helpful assistant.",
    model=openai_gpt4_mini,
)
# TODO: create query handler

async def main():
    runner = Runner.run_streamed(
        starting_agent=generic_agent,
        input="Hello, how are you?",
        
    )
    async for event in runner.stream_events():
        if isinstance(event, RawResponsesStreamEvent):
            if event.data.type == "response.output_text.delta":
                print(event.data.delta, flush=True, end="")
        elif isinstance(event, AgentUpdatedStreamEvent):
            logger.info(f"Agent updated: {event.new_agent.name}")
        elif isinstance(event, RunItemStreamEvent):
            logger.info(f"Run item: {event.item.type}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())