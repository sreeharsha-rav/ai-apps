from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from openai.types.responses import (
    ResponseTextDeltaEvent, 
    ResponseOutputItemDoneEvent
)
from app.services.llm import OpenAIQueryHandler
from app.core.store import LocalJSONChatStore

def chat_with_openai(system_instruction: str):
    console = Console()
    handler = OpenAIQueryHandler()
    
    # Initialize Persistent Store
    store = LocalJSONChatStore("chat_history.json")
    
    console.print(Panel("[bold green]Chat started![/bold green] Type 'exit' or 'quit' to end.\n[yellow]Type 'clear' to clear chat history.[/yellow]", 
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
                console.print(Panel("[bold yellow]Chat history cleared![/bold yellow]", border_style="yellow"))
                continue
            
            # Create user message object and store it
            user_item = {
                "role": "user",
                "content": [{"type": "input_text", "text": user_message}]
            }
            store.add_item(user_item)
            
            # Stream and display assistant response
            assistant_text_buffer = ""
            console.print()  # Add spacing
            
            with Live(Panel(Markdown("..."), title="Assistant", border_style="green"), refresh_per_second=10, console=console) as live:
                for event in handler.get_streaming_response(system_instruction, store.get_history()):
                    
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

            # End of stream for this turn
            
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting...[/bold red]")

if __name__ == "__main__":
    system_instruction = "You are a helpful assistant with access to Shopify Catalog API to fetch product details."
    chat_with_openai(system_instruction)
