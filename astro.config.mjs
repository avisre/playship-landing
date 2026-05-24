// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  site: "https://playship.pro",
  integrations: [
    sitemap({
      // /og is a screenshot-only route used to generate social previews.
      // It must NOT appear in the sitemap. See src/pages/og.astro and OG_ASSETS.md.
      filter: (page) => !page.includes("/og"),
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
