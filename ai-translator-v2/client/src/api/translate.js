import { TRANSLATE_BASE_URL, GOOGLE_TRANSLATE_API_KEY } from "./config";

/*
Translates the text into the target language. "text" can be a string for
translating a single piece of text, or an array of strings for translating
multiple texts.
*/

const translateText = async (text, source, target) => {
  try {
    console.log(`Translating text: ${text} from ${source} to ${target}`);
    const response = await fetch(TRANSLATE_BASE_URL, {
      method: "POST",
      headers: {
        "X-goog-api-key": GOOGLE_TRANSLATE_API_KEY,
        "Content-Type": "application/json; charset=utf-8",
      },
      body: JSON.stringify({
        q: text,
        target: target,
        source: source,
        format: "text",
      }),
    });

    if (!response.ok) {
      console.error("Translation failed:", response);
      throw new Error(`Translation failed: ${response.status}`);
    }

    const data = await response.json();
    return data.data.translations[0].translatedText;
  } catch (error) {
    console.error("Translation error:", error);
    throw error;
  }
};

export default translateText;
