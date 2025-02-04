// Imports the Google Cloud client library
const textToSpeech = require("@google-cloud/text-to-speech");
const fs = require("fs");
const util = require("util");

// Creates a client
const client = new textToSpeech.TextToSpeechClient();

async function listVoices() {
  // Lists the available voices
  const [result] = await client.listVoices({});
  const voices = result.voices;

  console.log("Voices:", voices);
}

async function synthesizeText() {
  // Construct the request
  const text = "My name is Harsha";
  const outputFile = "tts_outputs/output1.mp3";

  const request = {
    input: { text: text },
    voice: { languageCode: "en-US", ssmlGender: "FEMALE" },
    audioConfig: { audioEncoding: "MP3" },
  };
  const [response] = await client.synthesizeSpeech(request);
  const writeFile = util.promisify(fs.writeFile);
  await writeFile(outputFile, response.audioContent, "binary");
  console.log(`Audio content written to file: ${outputFile}`);
}

async function main() {
  //await listVoices();
  //await quickStart();
  await synthesizeText();
}

main();
