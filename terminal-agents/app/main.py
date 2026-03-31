import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from openai.types.responses import (
    ResponseTextDeltaEvent, 
    ResponseOutputItemDoneEvent,
    ResponseOutputMessage
)
from agents import Runner, RawResponsesStreamEvent, AgentUpdatedStreamEvent, RunItemStreamEvent
from app.core.llm import OpenAIQueryHandler
from app.core.agents import generic_agent
from app.core.store import LocalJSONChatStore, LocalJSONContextStore
from app.core.prompts import CURRENT_SYSTEM_PROMPT
from app.commands import COMMANDS

def render_history(console: Console, history: list):
    """Renders the chat history to the console."""
    if not history:
        console.print("[yellow]No chat history found.[/yellow]")
        return

    for item in history:
        if isinstance(item, dict):
            role = item.get("role")
            item_type = item.get("type")
            content = item.get("content", [])
            
            if role == "user":
                text = ""
                for part in content:
                    if part.get("type") == "input_text":
                        text += part.get("text", "")
                if text:
                    console.print(Panel(text, title="You", border_style="cyan"))
            
            elif role == "assistant" or item_type == "message":
                text = ""
                for part in content:
                    # The OpenAI response API uses "output_text" for message parts
                    if part.get("type") in ["text", "output_text"]:
                        text += part.get("text", "")
                if text:
                    console.print(Panel(Markdown(text), title="Assistant", border_style="green"))
            
            # Optional: Add indicators for tools
            # elif item_type == "mcp_call":
            #     console.print(f"[dim]Tool Call: {item.get('name')}[/dim]")

def chat_with_llm():
    console = Console()
    system_instruction = CURRENT_SYSTEM_PROMPT
    handler = OpenAIQueryHandler(system_instruction)
    store = LocalJSONChatStore("chat_history.json")
    context_store = LocalJSONContextStore("chat_context.json")

    context = context_store.get_context()
    
    console.print(Panel("[bold green]Chat started![/bold green] Type 'load' to load chat history.\n"
                       "Type 'exit' or 'quit' to end.\n"
                       "[yellow]Type 'clear' to clear chat history.[/yellow]\n"
                       "[cyan]Notion commands: notion-login, notion-status, notion-logout, notion-refresh[/cyan]\n"
                       "[cyan]Shopify commands: shopify-login, shopify-status, shopify-logout, shopify-refresh[/cyan]", 
                       title="OpenAI Chat", border_style="cyan"))
    
    try:
        while True:
            # Get user input
            user_message = console.input("\n[bold blue]You:[/bold blue] ").strip()
            
            if not user_message:
                continue
                
            if user_message.lower() in {"exit", "quit"}:
                console.print(Panel("[yellow]Chat ended.[/yellow]", border_style="yellow"))
                break

            if user_message.lower() == "clear":
                store.clear()
                context_store.clear()
                context = context_store.get_context()
                console.print(Panel("[bold yellow]Chat history and context cleared![/bold yellow]", border_style="yellow"))
                continue

            if user_message.lower() == "load":
                context = context_store.get_context()
                render_history(console, store.get_history())
                continue

            if user_message.lower() in COMMANDS:
                cmd_handler = COMMANDS[user_message.lower()]
                cmd_handler(console)
                continue

            console.print(Panel(Markdown(user_message), title="You", border_style="cyan"))
            
            # Create user message object and store it
            user_item = {
                "role": "user",
                "content": [{"type": "input_text", "text": user_message}]
            }
            store.add_item(user_item)

            console.print()  # Add spacing
            
            try:
                with Live(Panel(Markdown("..."), title="Assistant", border_style="green"), refresh_per_second=10, console=console) as live:
                    assistant_text_buffer = ""
                    for event in handler.get_streaming_response(store.get_history()):
                        
                        # 1. Update UI (Text Deltas ONLY)
                        if isinstance(event, ResponseTextDeltaEvent):
                            assistant_text_buffer += event.delta
                            live.update(Panel(Markdown(assistant_text_buffer), 
                                             title="Assistant", border_style="green"))
                        
                        # 2. Update History (Completed Output Items)
                        elif isinstance(event, ResponseOutputItemDoneEvent):
                            # Store messages, function calls, and MCP calls to maintain full history
                            if event.item.type in ["message", "web_search_call", "function_call", "mcp_list_tools", "mcp_call", "mcp_approval_request"]: 
                                 store.add_item(event.item)
            except Exception as e:
                console.print(Panel(f"[bold red]Generation Error:[/bold red] {e}", border_style="red"))
                store.get_history().pop() # pop the user input since it failed
            
            # End of stream for this turn
            
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting...[/bold red]")

async def chat_with_agent():
    console = Console()
    
    # TODO: update to Agent session storage
    store = LocalJSONChatStore("agent_history.json")
    context_store = LocalJSONContextStore("agent_context.json")

    context = context_store.get_context()
    
    console.print(Panel("[bold green]Agent started![/bold green] Type 'load' to load agent history.\n"
                       "Type 'exit' or 'quit' to end.\n"
                       "[yellow]Type 'clear' to clear agent history.[/yellow]\n"
                    #    "[cyan]Notion commands: notion-login, notion-status, notion-logout, notion-refresh[/cyan]\n"
                    #    "[cyan]Shopify commands: shopify-login, shopify-status, shopify-logout, shopify-refresh[/cyan]", 
                       , title="OpenAI Agent Chat", border_style="cyan"))
    
    try:
        while True:
            # Get user input
            try:
                user_message = console.input("\n[bold blue]You:[/bold blue] ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n")
                console.print(Panel("[yellow]Chat ended by user interruption.[/yellow]", border_style="yellow"))
                break
            
            if not user_message:
                continue
                
            if user_message.lower() in {"exit", "quit"}:
                console.print(Panel("[yellow]Chat ended.[/yellow]", border_style="yellow"))
                break

            if user_message.lower() == "clear":
                store.clear()
                context_store.clear()
                context = context_store.get_context()
                console.print(Panel("[bold yellow]Chat history and context cleared![/bold yellow]", border_style="yellow"))
                continue

            if user_message.lower() == "load":
                context = context_store.get_context()
                render_history(console, store.get_history())
                continue

            if user_message.lower() in COMMANDS:
                cmd_handler = COMMANDS[user_message.lower()]
                cmd_handler(console)
                continue

            console.print(Panel(Markdown(user_message), title="You", border_style="cyan"))
            
            # Create user message object and store it
            user_item = {
                "role": "user",
                "content": [{"type": "input_text", "text": user_message}]
            }
            store.add_item(user_item)

            console.print()  # Add spacing
            
            try:
                with Live(Panel(Markdown("..."), title=f"[bold green]{generic_agent.name}[/bold green]", border_style="green"), refresh_per_second=10, console=console) as live:
                    text_buffer = ""
                    result = Runner.run_streamed(
                        starting_agent=generic_agent,
                        input=store.get_history()
                    )
                    async for event in result.stream_events():
                        
                        # 1. Update UI (Text Deltas ONLY)
                        if isinstance(event, RawResponsesStreamEvent):
                            if isinstance(event.data, ResponseTextDeltaEvent):
                                text_buffer += event.data.delta
                                live.update(Panel(Markdown(text_buffer), 
                                                title=f"[bold green]{generic_agent.name}[/bold green]", border_style="green"))
                        
                        # 2. Update History (Completed Output Items)
                        elif isinstance(event, RunItemStreamEvent):
                            if isinstance(event.item.raw_item, ResponseOutputMessage):      # TODO: extend to mcp call, tool call, etc
                                store.add_item(event.item.raw_item)
            except (KeyboardInterrupt, asyncio.CancelledError):
                console.print(Panel("[yellow]Generation interrupted by user.[/yellow]", border_style="yellow"))
                break
            except Exception as e:
                import traceback
                # Provide a more detailed error message
                error_details = f"{type(e).__name__}: {str(e)}"
                console.print(Panel(f"[bold red]Generation Error:[/bold red]\n{error_details}", border_style="red"))
                if store.get_history():
                    store.get_history().pop() # pop the user input since it failed
            
            # End of stream for this turn
            
    except Exception as e:
        console.print(Panel(f"[bold red]Critical Session Error:[/bold red] {str(e)}", border_style="red"))
    finally:
        console.print("\n[bold dim]Agent session closed.[/bold dim]")

if __name__ == "__main__":
    # chat_with_llm()
    try:
        asyncio.run(chat_with_agent())
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass