import type { Message } from "~/types/message.model"
import { defineStore } from 'pinia'

/**
 * This is a simple chat store that holds chat messages and provides methods to send messages
 */
export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [] as Message[],    // Array of chat messages
    isLoading: false,        // Indicates if the chat is currently loading  a message
    error: null as Error | null // Holds the last error that occurred
  }),
  getters: {
    // This is a simple getter that returns true if there are messages
    hasMessages: (state) => state.messages.length > 0,

    // This is a simple getter that returns the last message
    lastMessage(): Message | undefined {
      return this.messages[this.messages.length - 1]
    }
  },
  actions: {
    // Simple action to add a message to the chat
    addMessage(message: Omit<Message, 'id'>) {
      this.messages.push({ 
        ...message, 
        id: this.messages.length + 1
      })
    },

    // This is an action that sends a message
    async sendMessage(content: string) {
      this.addMessage({ 
        role: 'user', 
        content: content,
        processing: false
      })

      this.isLoading = true
      this.addMessage({ 
        role: 'assistant', 
        content: '',
        processing: true
      })

      try {
        // TODO: Implement the actual API call
        const response = await new Promise((resolve, reject) => {
          setTimeout(() => {
            console.log("Message sent to server:", content)
            resolve("This is a response from the server")
          }, 2000); // Simulate 1 second delay
        });

        // update the last message with the response
        const lastMessage = this.lastMessage
        if (lastMessage) {
          lastMessage.content = response as string
          lastMessage.processing = false
        }
      } catch (error) {
        console.error(`Failed to send message: ${error}`)
        this.error = error as Error
      } finally {
        this.isLoading = false
      }
    },

    // This is a simple example of a method that clears all messages
    clearMessages() {
      this.messages = []
    }
  }
})