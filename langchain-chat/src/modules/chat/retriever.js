import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase';
import { OpenAIEmbeddings } from '@langchain/openai';
import { OPENAI_API_KEY } from '../../config/openai';
import { supabase } from '../../config/supabase';

const embeddings = new OpenAIEmbeddings({
  apiKey: OPENAI_API_KEY,
  model: 'text-embedding-ada-002',
});

const vectorStore = new SupabaseVectorStore(embeddings, {
  client: supabase, // client from config/supabase.js
  tableName: 'documents',
  queryName: 'match_documents',
});

const retriever = vectorStore.asRetriever();

export { retriever };
