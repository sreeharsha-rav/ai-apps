import { ThemeProvider } from "@/components/theme/theme-provider";
import { BrowserRouter, Routes, Route } from "react-router";
import { RootLayout } from "@/components/layout/root-layout";
import { ChatPage } from "@/pages/chat-page";

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider defaultTheme="dark" storageKey="ui-theme">
        <Routes>
          <Route element={<RootLayout />}>
            <Route index element={<ChatPage />} />
            <Route path="chat">
              <Route path="new" element={<ChatPage />} />
              <Route path=":id" element={<ChatPage />} />
            </Route>
          </Route>
        </Routes>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
