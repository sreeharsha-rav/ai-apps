import { TextLoader } from "langchain/document_loaders/fs/text";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";

/** Load and split a text file
 * @param {string} filePath - The path to the text file to load and split
 * @returns {Promise<Array<Document>>} - The split documents
 */
export async function loadAndSplitTextFile(filePath) {
    // Create a TextLoader instance
    const loader = new TextLoader(filePath);
    // Load the document
    const docs = await loader.load();
  
    // Create a text splitter
    const textSplitter = new RecursiveCharacterTextSplitter({
      chunkSize: 500,
      chunkOverlap: 50,
      separators: ["\n\n", "\n", " ", ""]  // prioritize splitting at newlines
    });
  
    // Split the loaded document
    const splitDocs = await textSplitter.splitDocuments(docs);
    console.log('Successfully split the document');
  
    // Print the split documents
    // splitDocs.forEach((doc, index) => {
    //   console.log(`Chunk ${index + 1}:`);
    //   console.log(doc.pageContent);
    //   console.log("---");
    // });

    return splitDocs;
  }