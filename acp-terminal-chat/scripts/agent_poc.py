import asyncio
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, OpenAIResponsesModel, Runner, RawResponsesStreamEvent, AgentUpdatedStreamEvent, RunItemStreamEvent
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from app.core.config import OPENAI_API_KEY


openai_gpt4_1_mini = OpenAIResponsesModel(
    model="gpt-4.1-mini",
    openai_client=AsyncOpenAI(api_key=OPENAI_API_KEY)
)

assistant_agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=openai_gpt4_1_mini,
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    model=openai_gpt4_1_mini,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    model=openai_gpt4_1_mini,
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    model=openai_gpt4_1_mini,
)
    
async def run_agent_loop():
    console = Console()
    history = []
    current_agent = triage_agent
    
    console.print(Panel(
        "[bold green]Chat started![/bold green] Type 'exit' or 'quit' to end.\n"
        "[dim]You can ask questions related to history or math.[/dim]", 
        title="Multi-Agent Tutor",
        border_style="cyan"
    ))
    
    try:
        while True:
            # Get user input
            user_message = console.input("\n[bold blue]You:[/bold blue] ").strip()
            if not user_message:
                continue
            if user_message.lower() in {"exit", "quit"}:
                console.print(Panel("[yellow]Chat ended.[/yellow]", border_style="yellow"))
                break
            history.append({"role": "user", "content": user_message})
            
            # Stream and display assistant response
            assistant_content = ""
            active_agent = current_agent
            console.print()  # Add spacing
            with Live(
                Panel(Markdown("Thinking..."), title=f"🤖 {active_agent.name}", border_style="green"), refresh_per_second=10, console=console) as live:
                agent_response = Runner.run_streamed(
                    starting_agent=current_agent,
                    input=history,
                )
                async for event in agent_response.stream_events():
                    
                    # Handle text streaming
                    if isinstance(event, RawResponsesStreamEvent):
                        data = event.data
                        if isinstance(data, ResponseTextDeltaEvent):
                            assistant_content += data.delta
                            live.update(Panel(
                                Markdown(assistant_content),
                                title=f"🤖 {active_agent.name}", 
                                border_style="green"
                            ))
                    
                    # Handle agent updates (handoffs)
                    elif isinstance(event, AgentUpdatedStreamEvent):
                        active_agent = event.new_agent
                        console.print(Panel(
                            f"[cyan]→ Routing to: [bold]🤖 {active_agent.name}[/bold][/cyan]",
                            border_style="cyan",
                            padding=(0, 2)
                        ))

                    # Handle tool calls (if any)
                    elif isinstance(event, RunItemStreamEvent):
                        if event.item.type == "tool_call_item":
                            tool_name = str(event.item.raw_item)
                            console.print(Panel(
                                f"[magenta]🔧 Calling tool: [bold]{tool_name}[/bold][/magenta]",
                                border_style="magenta",
                                padding=(0, 2)
                            ))
                        elif event.item.type == "tool_call_output_item":
                            output_preview = str(event.item.raw_item)
                            console.print(Panel(
                                f"[yellow]📊 Tool output: {output_preview}[/yellow]",
                                border_style="yellow",
                                padding=(0, 2)
                            ))
                    
            current_agent = triage_agent  # Reset to triage agent for next turn
            history = agent_response.to_input_list()  # Update history with full conversation
            
    except KeyboardInterrupt:
        console.print("\n[bold red]Interrupted. Exiting...[/bold red]")    
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
    
if __name__ == "__main__":
    asyncio.run(run_agent_loop())
