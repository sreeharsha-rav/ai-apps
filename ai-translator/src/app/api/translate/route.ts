import { NextRequest, NextResponse } from 'next/server';
import { translateText } from '@/services/translationService';

/**
 * Handles the POST request for translation.
 *
 * @param req - The NextRequest object containing the request data.
 * @returns A NextResponse object with the translated text or an error message.
 */
export async function POST(req: NextRequest) {
  const { text, targetLanguage } = await req.json();

  if (!text || !targetLanguage) {
    return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
  }

  try {
    const translatedText = await translateText(text, targetLanguage);
    return NextResponse.json({ translatedText });
  } catch (error) {
    console.error('Translation error:', error);
    return NextResponse.json({ error: 'Translation failed' }, { status: 500 });
  }
}