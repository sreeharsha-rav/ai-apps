import { openai_client } from "@/lib/openai";

/**
 * Translates the given text into the specified target language.
 * 
 * @param text - The text to be translated.
 * @param targetLanguage - The target language to translate the text into.
 * @returns A Promise that resolves to the translated text.
 * @throws If the translation fails.
 */
export async function translateText(text: string, targetLanguage: string): Promise<any> {
  try {
    const response = await openai_client.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: `You are a translator. You will be provided with a sentence in English, and your task is to translate it into ${targetLanguage}.` },
        { role: "user", content: text }
      ],
    });
    return response.choices[0].message?.content || 'Translation failed';
  } catch (error) {
    console.error('Translation error:', error);
    throw new Error('Translation failed');
  }
}

/**
 * Translates the given text into the specified target language using a stream.
 * 
 * @param text - The text to be translated.
 * @param targetLanguage - The target language to translate the text into.
 * @returns An async generator that yields the translated text.
 * @throws If the translation fails.
 */
// export async function* translateTextStream(text: string, targetLanguage: string) {
//     try {
//       const stream = await openai_client.chat.completions.create({
//         model: "gpt-4o-mini",
//         messages: [
//           { role: "system", content: `You are a translator. You will be provided with a sentence in English, and your task is to translate it into ${targetLanguage}.` },
//           { role: "user", content: text }
//         ],
//         stream: true,
//       });
  
//       for await (const chunk of stream) {
//         const content = chunk.choices[0]?.delta?.content || '';
//         if (content) {
//           yield content;
//         }
//       }
//     } catch (error) {
//       console.error('Translation error:', error);
//       throw new Error('Translation failed');
//     }
// }