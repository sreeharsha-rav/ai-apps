import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

dotenv.config();

const SUPABASE_API_KEY = process.env.SUPABASE_API_KEY;
const SUPABASE_URL = process.env.SUPABASE_URL;

export const supabase = createClient(SUPABASE_URL, SUPABASE_API_KEY);
