import { ChatRequestBody, ChatResponseBody } from "~/types/chat.model"
import { processMessage } from "../services/chatService"

export default defineEventHandler(async (event) => {
  const body = await readBody<ChatRequestBody>(event)

  if (!body.question) {
    return {
      statusCode: 400,
      body: { reply: 'Failed to process request, please provide a question' },
      error: 'Missing question in request body'
    } as ChatResponseBody
  }

  try {
    const response = await processMessage(body.question);
    return {
      statusCode: 200,
      body: { reply: response }
    } as ChatResponseBody
  } catch (error) {
    return {
      statusCode: 500,
      body: { reply: 'Failed to process request, please try again later' },
      error: error instanceof Error ? error.message : 'An unknown error occurred'
    } as ChatResponseBody
  }
})