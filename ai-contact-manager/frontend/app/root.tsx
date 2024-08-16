import {
  Links,
  LiveReload,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "@remix-run/react";
import "./styles/tailwind.css";
import PrelineScript from "./components/ui/preline.client";

/**
 * Renders the layout for the application.
 * 
 * @param children - The content to be rendered within the layout.
 * @returns The layout component.
 */
export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        {children}
        <ScrollRestoration />
        <Scripts />
        {/* Add preline script on every page */}
        {PrelineScript && <PrelineScript />}
        <LiveReload />
      </body>
    </html>
  );
}

/**
 * The root component of the application.
 * Renders the Outlet component.
 */
export default function App() {
  return <Outlet />;
}
