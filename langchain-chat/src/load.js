import { splitFile } from './modules/fileInput/textSplitter.js';
import { generateEmbeddings } from './modules/fileInput/embeddingGenerator.js';

/**
 * Function to load document and generate embeddings
 */
async function fileInputProcessor(path) {
  try {
    const documents = await splitFile(path);
    await generateEmbeddings(documents);
  } catch (error) {
    console.error('Error:', error);
  }
}

// Load the document and generate embeddings
fileInputProcessor('./src/db/scrimba_info.txt');
