import { loadAndSplitTextFile } from './services/textSplitter.js';
import { createEmbeddings } from './services/embeddings.js';

/**
 * Main function to load, split, generate embeddings, and store them
 */
async function main() {
  try {
    // Load and split the text file
    const documents = await loadAndSplitTextFile("./src/db/scrimba_info.txt");

    // Generate embeddings and store them
    await createEmbeddings(documents);

    console.log('Embeddings generated and stored successfully');

  } catch (error) {
    console.error('Error:', error);
  }
}

// Run the main function
main();