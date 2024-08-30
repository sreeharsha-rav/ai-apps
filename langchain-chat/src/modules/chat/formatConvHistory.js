/**
 * Function to format the conversation history
 * @param {Array<string>} messages - The messages to format
 * @returns {string} - The formatted conversation history
 */
export function formatConvHistory(messages) {
  return messages
    .map((message, i) => {
      if (i % 2 === 0) {
        return `Human: ${message}`;
      } else {
        return `AI: ${message}`;
      }
    })
    .join('\n');
}
