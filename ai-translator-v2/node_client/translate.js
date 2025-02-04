// Imports the Google Cloud client library
const GOOGLE_TRANSLATE_API_KEY = "AIzaSyA1te51d_0QyzcVNghXJXeIFOyjqNoK1fg";
const TRANSLATE_BASE_URL =
  "https://translation.googleapis.com/language/translate/v2";

const text = "Hello, world!";
const target = "ru";
const source = "en";

const translateText = async (text, target, source) => {
  try {
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
      }),
    });

    if (!response.ok) {
      console.error("Translation failed:", response);
      throw new Error(`Translation failed: ${response.status}`);
    }

    const data = await response.json();
    console.log(data);
    return data.data.translations[0].translatedText;
  } catch (error) {
    console.error("Translation error:", error);
    throw error;
  }
};

const main = async () => {
  const translatedText = await translateText(text, target, source);
  console.log(translatedText);
};

main();
