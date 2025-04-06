import { useEffect, useState } from "react";
import { ThemeContext } from "@/components/theme/theme-context";

export function ThemeProvider({
  children,
  defaultTheme = "light",
  storageKey = "ui-theme",
  ...props
}: {
  children: React.ReactNode;
  defaultTheme?: "dark" | "light";
  storageKey?: string;
}) {
  const [theme, setTheme] = useState<"dark" | "light">(
    () => (localStorage.getItem(storageKey) as "dark" | "light") || defaultTheme
  );

  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove("light", "dark");
    root.classList.add(theme);
  }, [theme]);

  const value = {
    theme,
    setTheme: (theme: "dark" | "light") => {
      localStorage.setItem(storageKey, theme);
      setTheme(theme);
    },
  };

  return (
    <ThemeContext.Provider {...props} value={value}>
      {children}
    </ThemeContext.Provider>
  );
}
