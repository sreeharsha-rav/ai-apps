from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, OpenAIResponsesModel, Runner, RawResponsesStreamEvent, AgentUpdatedStreamEvent, RunItemStreamEvent
from core.config import OPENAI_API_KEY
from core.prompts import CURRENT_SYSTEM_PROMPT


openai_gpt5_mini = OpenAIResponsesModel(
    model="gpt-5-mini",
    openai_client=AsyncOpenAI(api_key=OPENAI_API_KEY)
)

shopping_agent = Agent(
    name="Shopping Agent",
    instructions=CURRENT_SYSTEM_PROMPT,
    model=openai_gpt5_mini,
    # tools=get_tool_definitions()
)

# TODO: create query handler