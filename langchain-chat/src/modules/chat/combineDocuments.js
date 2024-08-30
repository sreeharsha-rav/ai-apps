/**
 * Function to combine documents received from vector store
 * @param {Array<object>} docs - The documents to combine
 * @returns {string} - The combined documents
 */
export function combineDocuments(docs) {
  return docs.map((doc) => doc.pageContent).join('\n\n');
}
