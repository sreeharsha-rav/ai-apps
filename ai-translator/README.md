# AI Translator

A Next.js application that provides real-time language translation using gpt-4o-mini.

### Description

AI Translator is a web application that allows users to input text and receive translations in various languages. It features a chat-like interface for a seamless user experience.

### Features

- Real-time text translation
- Language selection
- Chat-like interface for input and output
- Responsive design

#### Technical Features

- Built with Next.js for server-side rendering
- Uses React for building the user interface
- Written in TypeScript for type safety
- Styled with Tailwind CSS for rapid development
- Chat input disabled while waiting for translation

## Development

### Project Structure

```
ai-translator/src/
├── app/
│   ├── api/
│   │   └── translate/
│   │       └── route.ts         # New API route for translation
│   ├── globals.css              # Global styles
│   ├── layout.tsx               # Main layout component
│   └── page.tsx                 # Main page component
├── components/
│   ├── AiChat.tsx               # Main chat component managing state and logic
│   ├── ChatInput.tsx            # Input component for user messages
│   ├── Header.tsx               # Header component
│   ├── LanguageSelector.tsx     # Component for selecting target language
│   └── Translation.tsx          # Components for displaying input and output messages
├── subframe/                    # Subframe UI components
├── services/
│   └── translationService.ts    # Translation service
├── lib/
│   └── openai.ts                # OpenAI client configuration
└── other files ...
```

### Technologies

- Next.js 14+ (App Router)
- React 18+
- OpenAI JS SDK
- TypeScript
- Tailwind CSS
- pnpm (Package Manager)

## Getting Started

1. Clone the repository:
   ```
   git clone 
   cd ai-translator
   ```

2. Install dependencies:
   ```
   pnpm install
   ```

3. Run the development server:
   ```
   pnpm dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Environment Variables

Create a `.env.local` file in the root directory and add the following variables:

```
NEXT_PUBLIC_API_URL=your_api_url_here
```

Replace `your_api_url_here` with the actual URL of your translation API.

## Contributing

Contributions are welcome! Please feel free to submit an issue to report a bug or request a feature. 
If you would like to contribute code, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
