# React + TypeScript + Vite Client

A modern React application built with TypeScript, Vite, and Tailwind CSS, featuring automated code formatting and linting.

## Features

- ⚡ **Vite** - Fast build tool and development server
- ⚛️ **React 19** - Latest React with TypeScript
- 🎨 **Tailwind CSS v4** - Utility-first CSS framework
- 🧹 **ESLint + Prettier** - Automated code formatting and linting
- 📦 **pnpm** - Fast, disk space efficient package manager
- 🎯 **Radix UI** - Headless UI components
- 🔧 **Shadcn/ui** - Re-usable components built on Radix UI

## Quick Start

```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev

# Format code
pnpm format

# Lint code
pnpm lint

# Build for production
pnpm build
```

## Available Scripts

| Script          | Description                            |
| --------------- | -------------------------------------- |
| `pnpm dev`      | Start development server               |
| `pnpm format`   | Format all files with Prettier         |
| `pnpm lint`     | Run ESLint checks                      |
| `pnpm lint:fix` | Auto-fix ESLint issues                 |
| `pnpm check`    | Run format + lint together             |
| `pnpm build`    | Format, lint, and build for production |
| `pnpm preview`  | Preview production build               |

## Code Quality

This project includes automated code formatting and linting:

- **Prettier** - Consistent code formatting
- **ESLint** - Code quality and error detection
- **TypeScript** - Type safety
- **Auto-format on save** - VS Code integration

### Prettier Configuration

```json
{
  "semi": false,
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

### Development Workflow

1. Code is automatically formatted on save in VS Code
2. ESLint shows errors and warnings in real-time
3. Run `pnpm check` before committing changes
4. Build process automatically formats and lints code

## Project Structure

```
src/
├── components/          # Reusable UI components
│   └── ui/             # Shadcn/ui components
├── lib/                # Utility functions
├── App.tsx             # Main application component
├── main.tsx            # Application entry point
└── index.css           # Global styles
```

## VS Code Integration

This project includes VS Code settings for optimal development experience:

- Auto-format on save with Prettier
- ESLint errors and warnings display
- Auto-fix ESLint issues on save

## Tech Stack

- **Frontend Framework**: React 19 + TypeScript
- **Build Tool**: Vite 7
- **Styling**: Tailwind CSS v4
- **UI Components**: Radix UI + Shadcn/ui
- **Code Quality**: ESLint + Prettier
- **Package Manager**: pnpm

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run `pnpm check` to ensure code quality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request
