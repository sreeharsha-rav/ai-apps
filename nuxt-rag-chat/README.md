# Nuxt 3 Minimal Starter

This project is a starter for creating a chatbot using NeonDB and OpenAI's gpt-4o model. It is built with Nuxt 3 and Tailwind CSS. It's designed to be easy to use and get started with.

## Features

- **Neon Postgres Integration**: The project uses Neon Postgres as a vectorized database to store and retrieve data with ease.
- **OpenAI Integration**: The project uses OpenAI's GPT-4o model to generate responses to user queries.
- **Nuxt 3**: The project is built with Nuxt 3, a modern web framework for building Vue.js applications.
- **Tailwind CSS**: The project uses Tailwind CSS, a utility-first CSS framework for building custom designs.
- **Easily Customizable**: The project is designed to be easy to customize and extend.
- **Easy Deployment**: The project is easy to deploy to cloudflare workers or any other serverless platform.

## Getting Started

### Prerequisites

- A [Neon](https://neon.tech/) account.
  - A Neon pgvector database.
- An [OpenAI](https://platform.openai.com/) account.

## Deployment

### Cloudflare 

- Deploy to cloudflare using NuxtHub
```bash
npx nuxthub deploy
```

## Setup

Make sure to install the dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm run dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm run build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm run preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.
