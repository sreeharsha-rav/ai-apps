import { ChatRequestBody, ChatResponseBody, Message, Role } from '~/types/chat.model'
import { defineStore } from 'pinia'
import { v4 as uuidv4 } from 'uuid'

/**
 * This is a simple chat store that holds chat messages and provides methods to send messages
 */
export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [] as Message[],
    isLoading: false, 
    error: null as Error | null
  }),

  getters: {
    hasMessages: (state) => state.messages.length > 0,
    lastMessage: (state) => state.messages[state.messages.length - 1],
    userMessages: (state) => state.messages.filter(message => message.role === Role.User),
    assistantMessages: (state) => state.messages.filter(message => message.role === Role.Assistant),
  },

  actions: {
    addMessage(message: Omit<Message, 'id'>) {
      this.messages.push({ 
        ...message, 
        id: uuidv4()
      })
    },

    async sendMessage(content: string) {
      this.isLoading = true
      this.error = null

      try {
        this.addMessage({
          role: Role.User,
          content,
          processing: false
        })

        this.addMessage({
          role: Role.Assistant,
          content: '',
          processing: true
        })

        const response = await this.fetchReply(content) as ChatResponseBody;

        const lastMessage = this.lastMessage
        if (lastMessage && lastMessage.role === Role.Assistant) {
          lastMessage.content = response.body.reply
          lastMessage.processing = false
        }
      } catch (error) {
        console.error(`Failed to send message: ${error}`)
        this.error = error instanceof Error ? error : new Error('An unknown error occurred')

        const lastMessage = this.lastMessage
        if (lastMessage && lastMessage.role === Role.Assistant) {
          lastMessage.content = 'An error occurred while processing your request, please try again'
          lastMessage.processing = false
        }
      } finally {
        this.isLoading = false
      }
    },

    async fetchReply(content: string) {
      try {
        const response = await $fetch<ChatResponseBody>('/api/chat', {
          method: 'POST',
          body: { question: content } as ChatRequestBody,
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (!response) {
          throw new Error('No data received from server')
        }

        if (response.error) {
          throw new Error(response.error)
        }

        if (response.statusCode !== 200) {
          throw new Error(`Failed to send message: ${response.body.reply}`)
        }

        return response
      } catch (error) {
        throw new Error(error instanceof Error ? error.message : 'An unknown error occurred')
      }
    },
    
    clearMessages() {
      this.messages = []
    }
  }
})