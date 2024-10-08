import { HfInference } from "npm:@huggingface/inference";
import "jsr:@std/dotenv/load";

/**
 * Creates a new instance of HfInference with the provided API key.
 * 
 * @param apiKey - The API key to be used for authentication.
 */
const hf = new HfInference(Deno.env.get("HF_API_KEY"));
const out = await hf.chatCompletion({
	model: "microsoft/Phi-3-mini-4k-instruct",
	messages: [{ role: "user", content: "Tell me a dad joke" }],
	max_tokens: 500,
	temperature: 0.5,
  });
// for await (const chunk of inference.chatCompletionStream({
// 	model: "microsoft/Phi-3-mini-4k-instruct",
// 	messages: [{ role: "user", content: "Can you tell me a joke about dynosaurus" }],
// 	max_tokens: 500,
// })) {
// 	Deno.stdout.write(new TextEncoder().encode(chunk.choices[0]?.delta?.content || ""));
// }


console.log(out);