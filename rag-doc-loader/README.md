# RAG Document Loader

This is a simple script to load a text document and generate vector embeddings for chunks of text.

The embeddings are generated using the `openai/text-embedding-3-small` model from [`openai`](https://platform.openai.com/docs/guides/embeddings/use-cases) in `1536` dimensions.

[`Neon`](https://neon.tech) is used as a vector database to store the embeddings.

[`Langchain`](https://js.langchain.com/v0.2/docs/integrations/vectorstores/neon/) is used seamlessly to generate embeddings and store them in `Neon`.

More info [langchain/community/neon/vectorstores/neon/neonpostgres](https://v02.api.js.langchain.com/classes/_langchain_community.vectorstores_neon.NeonPostgres.html)

## Prerequisites

- [Node.js](https://nodejs.org/en/)
- [pnpm](https://pnpm.io/)

## Installation

```bash
pnpm install
```

## Configuration

- Create a `.env` file in the root directory of the project.
- Add the following environment variables to the `.env` file:

```
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
NEON_CONNECTION_STRING=<YOUR_NEON_CONNECTION_STRING>
```

## Usage

```bash
pnpm start
```

## Challenges and Further Improvements

- Need better documents to generate embeddings from. The current document is a simple text document with no specific structure.
- The document loader is optimized to load given text document at `./src/db/neon_info.txt`. This can be improved to accept any text document.
- More cleaning and preprocessing can be done to the text before generating embeddings.

## Contributing

Feel free to contribute to this project. Please create an issue or a pull request with your suggestions or improvements.

## License

This project is under MIT license.