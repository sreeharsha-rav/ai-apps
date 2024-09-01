import { aiSingleton } from "../utils/aiSingleton";

const conversations: string[] = [];   // Store the conversation history temporarily for the current session

export async function processMessage(question: string): Promise<string> {
  try {
    const chain = await aiSingleton.getChain();
    const response = await chain.invoke({
      question,
      conv_history: conversations.join('\n'),
    });

    conversations.push(`Human: ${question}`);
    conversations.push(`AI: ${response}`);

    return response;
  } catch (error) {
    console.error("Error in processMessage:", error);
    return "I'm sorry, but I encountered an error while processing your request. Please try again later.";
  }
}