import { Provider } from "jotai";
import LanguageSelector from "./components/language-selector";
import TranslationInput from "./components/translation-input";
import TranslationOutput from "./components/translation-output";

function App() {
  return (
    <Provider>
      <div className="container mx-auto max-w-md h-screen p-4">
        {/* Top Nav */}
        <div className="navbar bg-base-100 rounded mb-4">
          <a className="px-2 font-bold text-xl">Translate</a>
        </div>

        <div className="flex flex-col items-center gap-4 max-h-2/3 h-full rounded-lg p-4 bg-base-300">
          {/* Input */}
          <TranslationInput />
          <div className="divider" />
          {/* Output */}
          <TranslationOutput />
        </div>
        <div className="flex flex-col items-center gap-4 max-h-1/3 h-full rounded-lg p-4 shadow-lg">
          {/* Language Selector */}
          <LanguageSelector />
          {/* Voice Control */}
        </div>
      </div>
    </Provider>
  );
}

export default App;
