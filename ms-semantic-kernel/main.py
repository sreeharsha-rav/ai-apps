import asyncio
import traceback
from semantic_kernel import Kernel
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import AzureChatPromptExecutionSettings
from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)
from utils import CustomLogger


logger = CustomLogger()

async def main():
    try:
        kernel = Kernel()
        logger.info("Kernel initialized successfully.")
        
        chat_completion = AzureChatCompletion(
            api_key=AZURE_OPENAI_API_KEY,
            deployment_name=AZURE_OPENAI_DEPLOYMENT,
            api_version="2025-01-01-preview",
            base_url="https://ai-devsreeharsha1952ai664574680213.cognitiveservices.azure.com/openai/",
        )
        kernel.add_service(chat_completion)
        logger.info("Azure OpenAI Chat Completion service added to kernel.")
        
        prompt_execution_settings = AzureChatPromptExecutionSettings()
        logger.info("Azure Chat Prompt Execution Settings initialized.")
        
        history = ChatHistory()
        logger.info("Chat history initialized. Starting chat loop.")
        
        print("\n --- Welcome to the Azure OpenAI Chat! Type 'exit' or 'quit' to end the chat. --- \n")
        
        while True:
            user_input = input("User >  ")
            if user_input.lower() in {"exit", "quit"}:
                logger.info("Exiting the chat. Goodbye!")
                break
            
            history.add_user_message(user_input)
            
            response = await chat_completion.get_chat_message_content(
                chat_history=history,
                settings=prompt_execution_settings,
                kernel=kernel
            )
            print(f"Assistant >  {response}")
            
            if response is not None:
                history.add_message(response)
            else:
                logger.warning("Received an empty response from the assistant.")
    except Exception as e:
        logger.critical(f"ERROR: {e} - traceback: {traceback.format_exc()}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
