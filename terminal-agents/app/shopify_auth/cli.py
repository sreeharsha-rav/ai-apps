import time
from app.config.settings import SHOPIFY_CLIENT_ID, SHOPIFY_CLIENT_SECRET
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

from app.shopify_auth.client import exchange_credentials_for_token
from app.shopify_auth.storage import save_tokens, load_tokens, delete_tokens

def handle_login(console: Console):
    """Execute the Shopify Client Credentials login flow."""
    console.print(Panel.fit(
        "[bold green]🛍️ Shopify Authentication[/bold green]\n"
        "Authenticate using Shopify Client ID and Secret.",
        border_style="green"
    ))
    
    # If config has them, we don't even need local variables here
    if not SHOPIFY_CLIENT_ID or not SHOPIFY_CLIENT_SECRET:
        client_id = console.input("[bold]Enter Shopify Client ID:[/bold] ").strip()
        client_secret = console.input("[bold]Enter Shopify Client Secret:[/bold] ", password=True).strip()
    else:
        client_id = SHOPIFY_CLIENT_ID
        client_secret = SHOPIFY_CLIENT_SECRET
        
    if not client_id or not client_secret:
        console.print("[bold red]❌ Client ID and Secret are required.[/bold red]")
        return
        
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            task1 = progress.add_task("[cyan]Authenticating with Shopify...", total=None)
            # exchange_credentials_for_token now loads from env by default
            tokens = exchange_credentials_for_token(
                client_id if client_id != SHOPIFY_CLIENT_ID else None,
                client_secret if client_secret != SHOPIFY_CLIENT_SECRET else None
            )
            progress.update(task1, completed=True)
            
            save_tokens(tokens, client_id, client_secret)
            console.print("✓ Tokens saved locally")
            
        console.print("\n[bold green]✅ Shopify Authentication successful![/bold green]")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Shopify Authentication failed:[/bold red] {e}")

def handle_status(console: Console):
    """Check Shopify authentication status."""
    tokens = load_tokens()
    
    if not tokens:
        console.print(Panel.fit(
            "[yellow]⚠ Not authenticated with Shopify[/yellow]\n"
            "Type [bold]shopify-login[/bold] to authenticate.",
            border_style="yellow"
        ))
        return
        
    token_age_ms = int(time.time() * 1000) - tokens.updated_at
    expires_in_ms = (tokens.expires_in or 3600) * 1000
    remaining_ms = expires_in_ms - token_age_ms
    remaining_seconds = remaining_ms // 1000
    
    table = Table(title="🛍️ Shopify Auth Status", show_header=True, header_style="bold green")
    table.add_column("Property", style="green")
    table.add_column("Value", style="white")
    
    if remaining_seconds <= 0:
        status = "[red]Expired[/red]"
        table.add_row("Status", status)
        table.add_row("Client ID", f"{tokens.client_id[:10]}...")
        console.print(table)
        console.print("\n[yellow]Token expired. Type [bold]shopify-refresh[/bold] to refresh.[/yellow]")
    elif remaining_seconds <= 300:
        status = "[yellow]Expiring Soon[/yellow]"
        table.add_row("Status", status)
        table.add_row("Expires In", f"{remaining_seconds // 60}m {remaining_seconds % 60}s")
        table.add_row("Client ID", f"{tokens.client_id[:10]}...")
        console.print(table)
        console.print("\n[yellow]Token expiring soon. Type [bold]shopify-refresh[/bold] to refresh.[/yellow]")
    else:
        status = "[green]✓ Authenticated[/green]"
        table.add_row("Status", status)
        table.add_row("Expires In", f"{remaining_seconds // 60}m {remaining_seconds % 60}s")
        table.add_row("Client ID", f"{tokens.client_id[:10]}...")
        console.print(table)

def handle_logout(console: Console):
    """Delete stored Shopify tokens."""
    tokens = load_tokens()
    
    if not tokens:
        console.print("[yellow]No Shopify tokens found. Already logged out.[/yellow]")
        return
    
    delete_tokens()
    console.print("[green]✓ Shopify tokens deleted successfully.[/green]")
    console.print("[dim]You have been logged out of Shopify.[/dim]")

def handle_refresh(console: Console):
    """Refresh Shopify access token."""
    tokens = load_tokens()
    
    if not tokens:
        console.print("[red]❌ No Shopify tokens found. Please run shopify-login first.[/red]")
        return
        
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task1 = progress.add_task("[cyan]Refreshing Shopify access token...", total=None)
            # exchange_credentials_for_token now loads from env by default
            new_tokens = exchange_credentials_for_token()
            progress.update(task1, completed=True)
            
            save_tokens(new_tokens, tokens.client_id, tokens.client_secret)
            
        console.print("[green]✓ Shopify Token refreshed successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Shopify Token refresh failed:[/red] {e}")
        console.print("[yellow]You may need to re-authenticate with [bold]shopify-login[/bold][/yellow]")
