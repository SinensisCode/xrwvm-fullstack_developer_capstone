import { defineConfig } from "vite";

export default defineConfig({
  root: "frontend", // La cartella dove si trova il codice sorgente
  build: {
    outDir: "../server/frontend/static", // La cartella dove generare i file di output
  },
});
