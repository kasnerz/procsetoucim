import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://procsetoucim.cz",
  trailingSlash: "always",
  // "Jak to děláme" became "O projektu" (user 2026-10-25); old links keep working.
  redirects: { "/metodika/": "/o-projektu/" },
  build: { format: "directory" },
  devToolbar: { enabled: false },
});
