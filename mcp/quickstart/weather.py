from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Dev")

@mcp.tool()
def get_weather(location: str) -> str:
    """
    Gets the current weather for a given location.
    
    Args:
        location (str): The location to get the weather for.
        
    Returns:
        str: A string describing the current weather.
    """
    # Placeholder implementation
    return f"The current weather in {location} is sunny with a temperature of 25°C."

if __name__ == "__main__":
    mcp.run()