# Langchain Chat Bot

A simple chat bot used to chat with document built using Langchain, OpenAI and Supabase.

![Langchain Chat](./public/langchain_chat_flow.png)

## Getting Started

### Technologies

- Node.js
- pnpm
- Supabase
- OpenAI
- Langchain

### Installation

1. Clone the repository and go to the project directory

```bash
git clone <repo-url>
cd langchain-chat
```

2. Install dependencies

```bash 
pnpm install
```

3. Create a `.env` file in the root directory and add the following environment variables

```bash
SUPABASE_API_KEY=your-supabase-api-key
SUPABASE_URL=your-supabase-url
OPENAI_API_KEY=your-openai-api-key
```

4. Run the development server

```bash
pnpm dev
```

## Credits

- This project was developed with the help of materials from [The Official Langchain Course](https://v2.scrimba.com/the-official-langchainjs-course-c02t) from [Scrimba](https://v2.scrimba.com/).