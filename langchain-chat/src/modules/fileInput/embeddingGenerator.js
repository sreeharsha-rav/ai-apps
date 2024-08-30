import { supabase } from '../../config/supabase.js';
import { OpenAIEmbeddings } from '@langchain/openai';
import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase';
import { OPENAI_API_KEY } from '../../config/openai.js';

/**
 * Function to create embeddings for the given documents
 * @param {Array<Document>} documents - The documents to create embeddings for
 */
export async function generateEmbeddings(documents) {
  const embeddings = new OpenAIEmbeddings({
    apiKey: OPENAI_API_KEY,
    model: 'text-embedding-ada-002',
  });
  const vectorStore = await SupabaseVectorStore.fromDocuments(
    documents,
    embeddings,
    {
      client: supabase,
      tableName: 'documents',
    }
  );
  console.log(`Successfully generated and stored embeddings`);
}
