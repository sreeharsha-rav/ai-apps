from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Analysis Prompt")

@mcp.prompt()
def analysis_prompt(topic: str) -> str:
    """
    Returns a prompt for analyzing a given topic.
    
    Args:
        topic (str): The topic to analyze.
    """
    return f"Please provide a detailed analysis of the following topic in 400 words: {topic}"
        
if __name__ == "__main__":
    mcp.run()
