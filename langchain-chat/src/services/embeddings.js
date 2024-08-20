import { supabase } from "../config/supabase.js";
import { OpenAIEmbeddings } from "@langchain/openai";
import { SupabaseVectorStore } from "@langchain/community/vectorstores/supabase";

export async function createEmbeddings(documents) {

    // Import the OpenAIEmbeddings class
    const embeddings = new OpenAIEmbeddings({
        apiKey: process.env.OPENAI_API_KEY,
        model: "text-embedding-ada-002"
    });

    // Load the embeddings
    const vectorStore = await SupabaseVectorStore.fromDocuments(
        documents,
        embeddings,
        {
            client: supabase,
            tableName: "documents",
        }
    );
    
    console.log(`Successfully generated and stored embeddings`);
}