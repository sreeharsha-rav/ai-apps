import json
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from openai.types.responses import (
    ResponseTextDeltaEvent,
    ResponseFunctionToolCallParam,
    ResponseFunctionToolCall,
    ResponseOutputItemDoneEvent
)
from openai.types.responses.response_output_item import McpCall
from openai.types.responses import ResponseFunctionToolCall
from app.services.llm import OpenAIQueryHandler
from app.services.checkout import CheckoutService
from app.models import ShoppingContext, Product  
from app.core.store import LocalJSONChatStore, LocalJSONContextStore
from app.core.prompts import CURRENT_SYSTEM_PROMPT

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

def chat_with_openai(system_instruction: str):
    console = Console()
    handler = OpenAIQueryHandler()
    checkout_service = CheckoutService()
    
    # Initialize Persistent Stores
    store = LocalJSONChatStore("chat_history.json")
    context_store = LocalJSONContextStore("shopping_context.json")
    
    # Load previous context
    context = context_store.get_context()
    
    console.print(Panel("[bold green]Chat started![/bold green] Type 'exit' or 'quit' to end.\n[yellow]Type 'clear' to clear history, 'load' to show previous history.[/yellow]", 
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
                context = context_store.get_context() # Reset local reference
                console.print(Panel("[bold yellow]Chat history and shopping context cleared![/bold yellow]", border_style="yellow"))
                continue

            if user_message.lower() == "load":
                render_history(console, store.get_history())
                continue

            console.print(Panel(user_message, title="You", border_style="cyan"))
            
            # Create user message object and store it
            user_item = {
                "role": "user",
                "content": [{"type": "input_text", "text": user_message}]
            }
            store.add_item(user_item)
            
            # Stream and display assistant response
            console.print()  # Add spacing

            max_turns = 3
            current_turn = 0
            
            with Live(Panel(Markdown("..."), title="Assistant", border_style="green"), refresh_per_second=10, console=console) as live:
                while current_turn < max_turns:
                    assistant_text_buffer = ""
                    seen_text = False
                    tool_executed = False

                    for event in handler.get_streaming_response(system_instruction, store.get_history()):
                        
                        # 1. Update UI (Text Deltas ONLY)
                        if isinstance(event, ResponseTextDeltaEvent):
                            seen_text = True
                            assistant_text_buffer += event.delta
                            live.update(Panel(Markdown(assistant_text_buffer), 
                                            title="Assistant", border_style="green"))
                        
                        # 2. Update History (Completed Output Items)
                        elif isinstance(event, ResponseOutputItemDoneEvent):

                            # Process function calls
                            if event.item.type == "function_call" or isinstance(event.item, ResponseFunctionToolCall):
                                store.add_item(event.item)
                                tool_executed = True
                                
                                args = json.loads(event.item.arguments)
                                tool_name = event.item.name
                                result = None
                                
                                if tool_name == "create_checkout_session":
                                    session = checkout_service.create_session(args["items"])
                                    context.checkout_session = session
                                    result = session.model_dump_json()
                                    
                                elif tool_name == "get_checkout_session":
                                    session = checkout_service.get_session(args["session_id"])
                                    if session:
                                        context.checkout_session = session
                                        result = session.model_dump_json()
                                    else:
                                        result = json.dumps({"error": "Session not found"})
                                        
                                elif tool_name == "update_checkout_session":
                                    session = checkout_service.update_session(
                                        session_id=args["session_id"],
                                        buyer=args.get("buyer"),
                                        fulfillment_address=args.get("fulfillment_address"),
                                        fulfillment_option_id=args.get("fulfillment_option_id")
                                    )
                                    if session:
                                        context.checkout_session = session
                                        result = session.model_dump_json()
                                    else:
                                        result = json.dumps({"error": "Session not found"})

                                elif tool_name == "complete_checkout_session":
                                    session = checkout_service.complete_session(
                                        session_id=args["session_id"],
                                        payment_data={"token": args["payment_token"], "provider": "stripe"}
                                    )
                                    if session:
                                        context.checkout_session = session
                                        result = session.model_dump_json()
                                    else:
                                        result = json.dumps({"error": "Session not found"})
                                        
                                if result:
                                    # Save context after update
                                    context_store.save(context)
                                    
                                    # Add tool output to history
                                    tool_output_item = {
                                        "type": "function_call_output",
                                        "call_id": event.item.call_id,
                                        "output": result
                                    }
                                    store.add_item(tool_output_item)

                            # Process MCP calls
                            if event.item.type == "mcp_call" and isinstance(event.item, McpCall):
                                store.add_item(event.item)
                                tool_executed = True
                                if event.item.name == "search_global_products":
                                    output = event.item.output
                                    if output:
                                        result = json.loads(output)
                                        context.products = [Product(**p) for p in result.get("offers", [])]
                                        context_store.save(context)
                                        
                                elif event.item.name == "get_global_product_details":
                                    output = event.item.output
                                    if output:
                                        result = json.loads(output)
                                        context.product_details = Product(**result.get("product", {}))
                                        context_store.save(context)
                                
                            # Store other
                            elif event.item.type in ["message", "mcp_list_tools"]: 
                                    store.add_item(event.item)

                    # End of stream for this turn
                    current_turn += 1

                    # Termination Condition 1: If text was generated, we assume the assistant is waiting for user.
                    if seen_text:
                        break
                    
                    # Termination Condition 2: If no tools were executed and no text (unlikely but possible), stop.
                    if not tool_executed:
                        break
                    
                    # If tools were executed but NO text, we loop again to give the assistant 
                    # a chance to see the tool outputs and respond or call more tools.
                    # (e.g., create_session -> (loop) -> text "I've created your cart")
                    live.update(Panel(Markdown("... (processing tool results) ..."), 
                                        title="Assistant", border_style="green"))
            
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting...[/bold red]")

if __name__ == "__main__":
    system_instruction = CURRENT_SYSTEM_PROMPT
    chat_with_openai(system_instruction)
