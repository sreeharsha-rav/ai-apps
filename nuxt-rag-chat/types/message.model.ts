/**
 * Message model that represents a chat message
 */
export interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  processing: boolean
}