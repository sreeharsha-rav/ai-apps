import { ChatOpenAI, OpenAIEmbeddings } from "@langchain/openai";
import { NeonPostgres } from "@langchain/community/vectorstores/neon";
import { combineDocuments } from "./formatters";
import { standaloneQuestionPrompt, answerQuestionPrompt } from "./prompts";
import { RunnablePassthrough, RunnableSequence } from "@langchain/core/runnables";
import { StringOutputParser } from "@langchain/core/output_parsers";

class AISingleton {
  private static instance: AISingleton;
  private chain: RunnableSequence | null = null;
  private initializationPromise: Promise<void> | null = null;

  private constructor() {}

  public static getInstance(): AISingleton {
    if (!AISingleton.instance) {
      AISingleton.instance = new AISingleton();
    }
    return AISingleton.instance;
  }

  public async getChain(): Promise<RunnableSequence> {
    if (this.chain) {
      return this.chain;
    }

    if (!this.initializationPromise) {
      this.initializationPromise = this.initializeChain();
    }

    await this.initializationPromise;
    return this.chain!;
  }

  private async initializeChain(): Promise<void> {
    const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
    const NEON_CONNECTION_STRING = process.env.NEON_CONNECTION_STRING;

    if (!OPENAI_API_KEY || !NEON_CONNECTION_STRING) {
      throw new Error('Missing environment variables');
    }

    const llm = new ChatOpenAI({
      apiKey: OPENAI_API_KEY,
      model: 'gpt-4o-mini',
    });

    const embeddings = new OpenAIEmbeddings({
      apiKey: OPENAI_API_KEY,
      dimensions: 1536,
      model: 'text-embedding-3-small',
    });

    const vectorStore = await NeonPostgres.initialize(embeddings, {
      connectionString: NEON_CONNECTION_STRING,
      tableName: 'vectorstore_documents', // Name of the table to store the document to retrieve
    });

    const retriever = vectorStore.asRetriever();

    const standaloneQuestionChain = standaloneQuestionPrompt
      .pipe(llm)
      .pipe(new StringOutputParser());

    const retrieverChain = RunnableSequence.from([
      (prevResult) => prevResult.standalone_question || prevResult,
      retriever,
      combineDocuments,
    ]);

    const answerQuestionChain = answerQuestionPrompt
      .pipe(llm)
      .pipe(new StringOutputParser())
      .pipe((output: string) => output.replace(/^answer:\s*/i, '').trim());

    this.chain = RunnableSequence.from([
      {
        standalone_question: standaloneQuestionChain,
        original_input: new RunnablePassthrough(),
      },
      async (input) => {
        const context = await retrieverChain.invoke(input.standalone_question);
        return {
          context: context,
          question: input.original_input.question,
          conv_history: input.original_input.conv_history,
        };
      },
      answerQuestionChain,
    ]);
  }
}

export const aiSingleton = AISingleton.getInstance();