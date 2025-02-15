import { generateText } from "ai";
import { createOpenAI as createGroq } from "@ai-sdk/openai";

const groq = createGroq({
  baseURL: "https://api.groq.com/openai/v1",
  apiKey: process.env["GROQ_API_KEY"],
});

export async function generateVocabularyFromLLM(category: string) {
  const prompt = `Generate a structured JSON output for Japanese vocabulary related to the theme "${category}". The output should be an array of objects, where each object represents a vocabulary item with the following structure:
  {
    "kanji": "Japanese word in kanji or kana",
    "romaji": "Romanized version of the word",
    "english": "English translation",
    "parts": [
      {
        "kanji": "Individual kanji or kana character",
        "romaji": ["Possible readings of the character"]
      },
      ...
    ]
  }
  Generate at least 5 vocabulary items and send back raw json and nothing else.

  Here is an example of bad output:
  {
    "kanji": "晴れ",
    "romaji": "hare",
    "english": "sunny",
    "parts": [
      {
        "kanji": "晴",
        "romaji": [
          "seki",
          "haru"
        ]
  ...
  }
  ^ The reason this is bad is because the parts of romaji that are shown do not represent the word. 
  Instead of listing out seki haru, it should just say ha because that is what the kanji is representing 
  for that word hare.

  Another reason this is bad is because it's missing the other part. 
  There should be 2 parts: one for ha and the other for re.

  Here are great examples with all of the parts broken up:
  {
    "kanji": "古い",
    "romaji": "furui",
    "english": "old",
    "parts": [
      { "kanji": "古", "romaji": ["fu", "ru"] },
      { "kanji": "い", "romaji": ["i"] }
    ]
  },
  {
    "kanji": "忙しい",
    "romaji": "isogashii",
    "english": "busy",
    "parts": [
      { "kanji": "忙", "romaji": ["i","so","ga"] },
      { "kanji": "し", "romaji": ["shi"] },
      { "kanji": "い", "romaji": ["i"] }
    ]
  },
  {
    "kanji": "新しい",
    "romaji": "atarashii",
    "english": "new",
    "parts": [
      { "kanji": "新", "romaji": ["a","ta","ra"] },
      { "kanji": "し", "romaji": ["shi"] },
      { "kanji": "い", "romaji": ["i"] }
    ]
  },
  {
    "kanji": "悪い",
    "romaji": "warui",
    "english": "bad",
    "parts": [
      { "kanji": "悪", "romaji": ["wa","ru"] },
      { "kanji": "い", "romaji": ["i"] }
    ]
  }

  ^ This is a good output because the word represents all the kanji and kana shown in the word.
  
  `;

  try {
    const { text } = await generateText({
      model: groq("gemma2-9b-it"),
      prompt: prompt,
    });
    console.log("===========================");
    console.log("text", text);
    console.log("===========================");
    // Parse the generated text as JSON
    const vocabularyData = JSON.parse(text);
    return vocabularyData;
  } catch (error) {
    console.error("Error generating vocabulary from LLM:", error);
    throw error;
  }
}
