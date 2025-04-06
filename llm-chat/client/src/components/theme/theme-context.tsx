"use client";

import { createContext } from "react";

type Theme = "dark" | "light";

type ThemeProviderState = {
  theme: Theme;
  setTheme: (theme: Theme) => void;
};

const initialState: ThemeProviderState = {
  theme: "light",
  setTheme: () => null,
};

export const ThemeContext = createContext<ThemeProviderState>(initialState);
