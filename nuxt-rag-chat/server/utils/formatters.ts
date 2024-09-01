// Utility functions
export function formatConvHistory(messages: string[]) {
  return messages
    .map((message, i) => {
      if (i % 2 === 0) {
        return `Human: ${message}`
      } else {
        return `AI: ${message}`
      }
    })
    .join('\n')
}

export function combineDocuments(docs: any[]) {
  return docs.map((doc: any) => doc.pageContent).join('\n\n')
}