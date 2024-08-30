import { retriever } from './modules/chat/retriever.js';
import { combineDocuments } from './modules/chat/combineDocuments.js';
import { formatConvHistory } from './utils/formatConvHistory.js';
import { OPENAI_API_KEY } from './config/openai.js';

document.addEventListener('submit', (e) => {
  e.preventDefault();
  progressConversation();
});

const llm = new ChatOpenAI({
  apiKey: OPENAI_API_KEY,
  model: 'gpt-4o-mini',
});

// Create a prompt template for the standalone question
const standaloneQuestionTemplate = `Given some conversation history (if any) and a question, convert the question to a standalone question. 
conversation history: {conv_history}
question: {question} 
standalone question:`;
const standaloneQuestionPrompt = PromptTemplate.fromTemplate(
  standaloneQuestionTemplate
);

// Create a prompt template for the answer
const answerTemplate = `You are a helpful and enthusiastic support bot who can answer a given question about Scrimba based on the context provided and the conversation history. Try to find the answer in the context. If the answer is not given in the context, find the answer in the conversation history if possible. If you really don't know the answer, say "I'm sorry, I don't know the answer to that." And direct the questioner to email help@scrimba.com. Don't try to make up an answer. Always speak as if you were chatting to a friend.
context: {context}
conversation history: {conv_history}
question: {question}
answer: `;
const answerPrompt = PromptTemplate.fromTemplate(answerTemplate);

// Create a standalone question chain
const standaloneQuestionChain = standaloneQuestionPrompt
  .pipe(llm)
  .pipe(new StringOutputParser());

// Create a retriever chain
const retrieverChain = RunnableSequence.from([
  (prevResult) => prevResult.standalone_question,
  retriever,
  combineDocuments,
]);

// Create an answer chain
const answerChain = answerPrompt.pipe(llm).pipe(new StringOutputParser());

// Create a chain to handle the entire conversation
const chain = RunnableSequence.from([
  {
    standalone_question: standaloneQuestionChain,
    original_input: new RunnablePassthrough(),
  },
  {
    context: retrieverChain,
    question: ({ original_input }) => original_input.question,
    conv_history: ({ original_input }) => original_input.conv_history,
  },
  answerChain,
]);

// Conversation history
const convHistory = [];

// Function to progress the conversation
async function progressConversation() {
  const userInput = document.getElementById('user-input');
  const chatbotConversation = document.getElementById(
    'chatbot-conversation-container'
  );
  const question = userInput.value;
  userInput.value = '';

  // add human message
  const newHumanSpeechBubble = document.createElement('div');
  newHumanSpeechBubble.classList.add('speech', 'speech-human');
  chatbotConversation.appendChild(newHumanSpeechBubble);
  newHumanSpeechBubble.textContent = question;
  chatbotConversation.scrollTop = chatbotConversation.scrollHeight;
  const response = await chain.invoke({
    question: question,
    conv_history: formatConvHistory(convHistory),
  });
  convHistory.push(question);
  convHistory.push(response);

  // add AI message
  const newAiSpeechBubble = document.createElement('div');
  newAiSpeechBubble.classList.add('speech', 'speech-ai');
  chatbotConversation.appendChild(newAiSpeechBubble);
  newAiSpeechBubble.textContent = response;
  chatbotConversation.scrollTop = chatbotConversation.scrollHeight;
}
