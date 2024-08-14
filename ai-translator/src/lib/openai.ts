// OpenAI Client Configuration

import OpenAI from 'openai';

export const openai_client = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});