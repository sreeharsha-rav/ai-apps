import os
import json
from typing import Optional, Any
from dotenv import load_dotenv
from openai import OpenAI
from src.config import logger

load_dotenv(dotenv_path=".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
logger.info(f"===(main)=== Loaded OPENAI_API_KEY: { '*' * 8 if OPENAI_API_KEY else None }")

llm_client = OpenAI(api_key=OPENAI_API_KEY)

def call_tool(tool_name: str, tool_args: Any, tool_map: dict) -> Any:
    """
    Executes a tool based on its name and arguments.
    
    Args:
        tool_name (str): The name of the tool to execute.
        tool_args (Any): The arguments to pass to the tool.
        tool_map (dict): A mapping of tool names to their corresponding functions.
        
    Returns:
        Any: The result returned by the tool function.
    """
    try:    
        if tool_name not in tool_map:
            raise ValueError(f"Tool {tool_name} not found in tool map.")
        
        tool_result = tool_map[tool_name](**tool_args)
        
        if tool_result is not None:
            logger.info(f"Tool '{tool_name}' executed successfully.")
            return tool_result
        else:
            logger.info(f"Tool '{tool_name}' executed successfully with no return value.")
            return None
    except ValueError as e:
        logger.error(f"Value error executing tool '{tool_name}': {e}")
        raise
    except TypeError as e:
        logger.error(f"Invalid arguments for tool '{tool_name}': {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error executing tool '{tool_name}': {e}")
        raise

def process_user_query(system_instruction: str, user_query: str, messages: list, llm_client: OpenAI, tools: list, tool_map: dict, max_turns: int = 5) -> Optional[dict]:
    """
    Process a user query using the LLM and available tools.
    
    Args:
        system_instruction (str): The system instruction for the LLM.
        user_query (str): The user's query.
        messages (list): The conversation history.
        llm_client (OpenAI): The OpenAI client instance.
        tools (list): The list of available tools.
        tool_map (dict): A mapping of tool names to their corresponding functions.
        max_turns (int): The maximum number of interaction turns.
        
    Returns:
        Optional[dict]: The final response from the LLM.
    """
    try:
        messages.append({"role": "user", "content": user_query})
        
        finish = False
        final_response = None
        turns = 0
        
        while not finish and turns < max_turns:
            turns += 1
            try:
                response = llm_client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        *messages
                    ],
                    tools=tools,
                    tool_choice="auto"
                )
                
                message = response.choices[0].message
                
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)
                        logger.info(f"Invoking tool: {tool_name} with args: {tool_args}")
                        
                        try:
                            tool_result = call_tool(tool_name, tool_args, tool_map)
                            
                            messages.append(message.model_dump())
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": tool_name,
                                "content": str(tool_result)
                            })
                        except Exception as e:
                            logger.error(f"Tool execution failed: {e}")
                            messages.append(message.model_dump())
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": tool_name,
                                "content": f"Error: {str(e)}"
                            })
                else:
                    final_response = message.model_dump()
                    messages.append({
                        "role": "assistant",
                        "content": message.content
                    })
                    finish = True
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse tool arguments: {e}")
                raise
            except Exception as e:
                logger.error(f"Error in LLM call (turn {turns}): {e}")
                raise
        
        if turns >= max_turns and not finish:
            logger.warning(f"Max turns ({max_turns}) reached without completion.")
        
        return final_response
        
    except Exception as e:
        logger.error(f"Fatal error processing query: {e}")
        raise
