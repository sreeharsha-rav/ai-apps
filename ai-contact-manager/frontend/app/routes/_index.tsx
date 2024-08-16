import type { MetaFunction } from "@remix-run/cloudflare";
import Footer from "../components/layout/Footer";
import Header from "../components/layout/Header";

export const meta: MetaFunction = () => {
  return [
    { title: "AI Contact Manager" },
    {
      name: "AI Contact Manager",
      content: "An AI-powered contact manager for email.",
    },
  ];
};

export default function Index() {
  return (
    <div className="font-sans p-4">
      <Header />
      <h1 className="text-3xl">Welcome to Remix on Cloudflare</h1>
      <ul className="list-disc mt-4 pl-6 space-y-2">
        <li>
          <a
            className="text-blue-700 underline visited:text-purple-900"
            target="_blank"
            href="https://remix.run/docs"
            rel="noreferrer"
          >
            Remix Docs
          </a>
        </li>
        <li>
          <a
            className="text-blue-700 underline visited:text-purple-900"
            target="_blank"
            href="https://developers.cloudflare.com/pages/framework-guides/deploy-a-remix-site/"
            rel="noreferrer"
          >
            Cloudflare Pages Docs - Remix guide
          </a>
        </li>
      </ul>
      <Footer />
    </div>
  );
}
