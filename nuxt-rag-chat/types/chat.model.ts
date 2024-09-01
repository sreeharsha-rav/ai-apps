/**
 * Message model that represents a chat message
 */
export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  processing: boolean
}

export enum Role {
  User = 'user',
  Assistant = 'assistant'
}

export interface ChatRequestBody {
  question: string;
}

export interface ChatResponse {
  reply: string;
}

export interface ChatResponseBody {
  statusCode: number;
  body: ChatResponse;
  error?: string;
}