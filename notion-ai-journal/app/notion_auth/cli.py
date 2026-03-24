import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from threading import Thread
from typing import Dict, Any

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

from app.notion_auth.client import (
    discover_oauth_metadata,
    register_client,
    create_authorization_url,
    exchange_code_for_tokens,
    refresh_access_token,
)
from app.notion_auth.storage import (
    save_tokens,
    load_tokens,
    delete_tokens,
)
from app.config import (
    NOTION_MCP_SERVER_URL,
    NOTION_CALLBACK_PORT,
    NOTION_CALLBACK_URI,
)


# Global state for callback (shared within this module)
_callback_result: Dict[str, Any] = {
    'code': None,
    'state': None,
    'error': None,
    'received': False
}

class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback."""
    
    def do_GET(self):
        """Handle GET request to /callback."""   
        parsed_url = urlparse(self.path)
        
        if parsed_url.path != '/callback':
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
            return
        
        # Parse query parameters
        params = parse_qs(parsed_url.query)
        code = params.get('code', [None])[0]
        state = params.get('state', [None])[0]
        error = params.get('error', [None])[0]
        error_description = params.get('error_description', [None])[0]
        
        if error:
            _callback_result['error'] = f"{error}: {error_description or 'Unknown error'}"
            _callback_result['received'] = True
            
            self.send_response(400)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            html = f"""
            <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h1 style="color: red;">Authorization Failed</h1>
                    <p>Error: {error}</p>
                    <p>{error_description or ''}</p>
                    <p>You can close this window.</p>
                </body>
            </html>
            """
            self.wfile.write(html.encode())
            return
        
        if code and state:
            _callback_result['code'] = code
            _callback_result['state'] = state
            _callback_result['received'] = True
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            html = """
            <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h1 style="color: green;">Authorization Successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                    <script>
                        // Auto-close after 3 seconds
                        setTimeout(() => {{ window.close(); }}, 3000);
                    </script>
                </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Missing code or state parameters')
    
    def log_message(self, format, *args):
        """Suppress server logs."""
        pass

def start_callback_server(console: Console):
    """Start temporary HTTP server for OAuth callback."""
    server = HTTPServer(('localhost', NOTION_CALLBACK_PORT), CallbackHandler)
    console.print(f"[dim]Callback server listening on {NOTION_CALLBACK_URI}[/dim]")
    
    # Run server in a thread
    server_thread = Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    
    return server

def handle_login(console: Console):
    """Execute the OAuth login flow."""  
    # Reset state
    _callback_result['code'] = None
    _callback_result['state'] = None
    _callback_result['error'] = None
    _callback_result['received'] = False

    console.print(Panel.fit(
        "[bold blue]🔐 Notion OAuth Authentication[/bold blue]\n"
        "Starting OAuth flow with dynamic client registration...",
        border_style="blue"
    ))
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # Step 1: Discovery
            task1 = progress.add_task("[cyan]1/7[/cyan] 🔍 Discovering OAuth metadata...", total=None)
            metadata = discover_oauth_metadata(NOTION_MCP_SERVER_URL)
            progress.update(task1, completed=True)
            console.print("✓ OAuth metadata discovered")
            
            # Step 2: Registration
            task2 = progress.add_task("[cyan]2/7[/cyan] 📝 Registering dynamic client...", total=None)
            credentials = register_client(metadata, NOTION_CALLBACK_URI)
            progress.update(task2, completed=True)
            console.print(f"✓ Client registered (ID: {credentials.client_id[:20]}...)")
            
            # Step 3: PKCE
            task3 = progress.add_task("[cyan]3/7[/cyan] 🔐 Generating PKCE security values...", total=None)
            from authlib.common.security import generate_token
            oauth_state = generate_token(32)
            progress.update(task3, completed=True)
            console.print("✓ PKCE values generated")
            
            # Step 4: Start callback server
            task4 = progress.add_task("[cyan]4/7[/cyan] 🌐 Starting local callback server...", total=None)
            server = start_callback_server(console)
            progress.update(task4, completed=True)
            console.print(f"✓ Server listening on port {NOTION_CALLBACK_PORT}")
            
            # Step 5: Create auth URL and open browser
            task5 = progress.add_task("[cyan]5/7[/cyan] 🚀 Opening browser for authorization...", total=None)
            auth_url, code_verifier = create_authorization_url(
                metadata=metadata,
                client_id=credentials.client_id,
                redirect_uri=NOTION_CALLBACK_URI,
                state=oauth_state,
                scopes=[]
            )
            progress.update(task5, completed=True)
            
            console.print("\n[yellow]Opening browser... Please authorize the application.[/yellow]")
            webbrowser.open(auth_url)
            
            # Step 6: Wait for callback
            task6 = progress.add_task("[cyan]6/7[/cyan] ⏳ Waiting for callback...", total=None)
            
            # Wait for callback with timeout
            timeout = 300  # 5 minutes
            start_time = time.time()
            while not _callback_result['received']:
                if time.time() - start_time > timeout:
                    raise TimeoutError("Authorization timeout after 5 minutes")
                time.sleep(0.5)
            
            progress.update(task6, completed=True)
            
            # Shutdown server
            server.shutdown()
            
            # Check for errors
            if _callback_result['error']:
                raise Exception(_callback_result['error'])
            
            # Validate state
            if _callback_result['state'] != oauth_state:
                raise Exception("State mismatch! Possible CSRF attack.")
            
            console.print("✓ Authorization code received")
            
            # Step 7: Exchange code for tokens
            task7 = progress.add_task("[cyan]7/7[/cyan] 🔄 Exchanging code for tokens...", total=None)
            tokens = exchange_code_for_tokens(
                code=_callback_result['code'],
                code_verifier=code_verifier,
                metadata=metadata,
                client_id=credentials.client_id,
                client_secret=credentials.client_secret,
                redirect_uri=NOTION_CALLBACK_URI
            )
            progress.update(task7, completed=True)
            
            # Save tokens
            save_tokens(
                tokens,
                client_id=credentials.client_id,
                client_secret=credentials.client_secret
            )
            console.print("✓ Tokens saved to .notion-tokens.json")
        
        console.print("\n[bold green]✅ Authentication successful![/bold green]")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Authentication failed:[/bold red] {e}")

def handle_status(console: Console):
    """Check authentication status."""
    tokens = load_tokens()
    
    if not tokens:
        console.print(Panel.fit(
            "[yellow]⚠ Not authenticated[/yellow]\n"
            "Type [bold]notion-login[/bold] to authenticate.",
            border_style="yellow"
        ))
        return
    
    # Calculate token age and expiry
    token_age_ms = int(time.time() * 1000) - tokens.updated_at
    expires_in_ms = (tokens.expires_in or 3600) * 1000
    remaining_ms = expires_in_ms - token_age_ms
    remaining_seconds = remaining_ms // 1000
    
    # Create status table
    table = Table(title="🔐 Notion Auth Status", show_header=True, header_style="bold cyan")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    if remaining_seconds <= 0:
        status = "[red]Expired[/red]"
        table.add_row("Status", status)
        table.add_row("Has Refresh Token", "✓" if tokens.refresh_token else "✗")
        console.print(table)
        console.print("\n[yellow]Token expired. Type [bold]notion-refresh[/bold] to refresh.[/yellow]")
    elif remaining_seconds <= 300:  # 5 minutes
        status = "[yellow]Expiring Soon[/yellow]"
        table.add_row("Status", status)
        table.add_row("Expires In", f"{remaining_seconds // 60} minutes {remaining_seconds % 60} seconds")
        table.add_row("Token Type", tokens.token_type)
        console.print(table)
        console.print("\n[yellow]Token expiring soon. Consider typing [bold]notion-refresh[/bold][/yellow]")
    else:
        status = "[green]✓ Authenticated[/green]"
        table.add_row("Status", status)
        table.add_row("Expires In", f"{remaining_seconds // 60} minutes {remaining_seconds % 60} seconds")
        table.add_row("Token Type", tokens.token_type)
        table.add_row("Client ID", f"{tokens.client_id[:20]}..." if tokens.client_id else "N/A")
        console.print(table)

def handle_logout(console: Console):
    """Delete stored tokens."""
    tokens = load_tokens()
    
    if not tokens:
        console.print("[yellow]No tokens found. Already logged out.[/yellow]")
        return
    
    delete_tokens()
    console.print("[green]✓ Tokens deleted successfully.[/green]")
    console.print("[dim]You have been logged out of Notion.[/dim]")

def handle_refresh(console: Console):
    """Refresh expired tokens."""
    tokens = load_tokens()
    
    if not tokens:
        console.print("[red]❌ No tokens found. Please login first.[/red]")
        return
    
    if not tokens.refresh_token:
        console.print("[red]❌ No refresh token available. Please re-authenticate.[/red]")
        return
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            task1 = progress.add_task("[cyan]Discovering OAuth metadata...", total=None)
            metadata = discover_oauth_metadata(NOTION_MCP_SERVER_URL)
            progress.update(task1, completed=True)
            
            task2 = progress.add_task("[cyan]Refreshing access token...", total=None)
            new_tokens = refresh_access_token(
                refresh_token=tokens.refresh_token,
                metadata=metadata,
                client_id=tokens.client_id,
                client_secret=tokens.client_secret
            )
            progress.update(task2, completed=True)
            
            # Save new tokens
            save_tokens(
                new_tokens,
                client_id=tokens.client_id,
                client_secret=tokens.client_secret
            )
        
        console.print("[green]✓ Token refreshed successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Token refresh failed:[/red] {e}")
        console.print("[yellow]You may need to re-authenticate with [bold]notion-login[/bold][/yellow]")
