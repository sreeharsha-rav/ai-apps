import dotenv from 'dotenv';
import { TextLoader } from 'langchain/document_loaders/fs/text';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { OpenAIEmbeddings } from "@langchain/openai";
import { NeonPostgres } from "@langchain/community/vectorstores/neon";

dotenv.config();

function preprocessText(content: string): string {
  return content
    .replace(/\n{3,}/g, '\n\n')  // Remove excessive newlines
    .split('\n')
    .map(line => line.trim())    // Trim whitespace from each line
    .join('\n')
    .trim();                     // Trim leading/trailing whitespace
}

async function splitFile(filePath: string) {
  const loader = new TextLoader(filePath);
  const docs = await loader.load();
  // Apply custom preprocessing on the loaded content
  docs.forEach(doc => {
    doc.pageContent = preprocessText(doc.pageContent);
  });

  const textSplitter = new RecursiveCharacterTextSplitter({
    chunkSize: 200,
    chunkOverlap: 50,
    separators: ['\n\n', '\n', ' ', ''], // prioritize splitting at newlines
    lengthFunction: (text) => text.split(/\s+/).length, // split by words
  });

  const splitDocs = await textSplitter.splitDocuments(docs);
  console.log('Successfully split the document');

  // splitDocs.forEach((doc, index) => {
  //   console.log(`Chunk ${index + 1}:`);
  //   console.log(doc.pageContent);
  //   console.log("---");
  // });
  console.log(`Split ${splitDocs.length} documents into chunks`);

  return splitDocs;
}


async function generateEmbeddings(documents: any) {
  const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
  if (!OPENAI_API_KEY) {
    throw new Error('OPENAI_API_KEY is not defined');
  }

  const embeddings = new OpenAIEmbeddings({
    apiKey: OPENAI_API_KEY,
    dimensions: 1536,
    model: 'text-embedding-3-small',
  });

  const NEON_CONNECTION_STRING = process.env.NEON_CONNECTION_STRING;
  if (!NEON_CONNECTION_STRING) {
    throw new Error('NEON_CONNECTION_STRING is not defined');
  }

  const vectorStore = await NeonPostgres.initialize(embeddings, {
    connectionString: NEON_CONNECTION_STRING,
  });

  const idsInserted = await vectorStore.addDocuments(documents);
  console.log(`Successfully inserted ${idsInserted.length} documents`);

  console.log(`Successfully generated and stored embeddings`);
}

async function main() {
  try {
    const filePath = 'src/db/neon_info.txt';  // Path to the file to be processed
    const splitDocs = await splitFile(filePath);
    await generateEmbeddings(splitDocs);
  } catch (error) {
    console.error("An error occurred:", error);
  }
}

main();