import { SimpleSearch } from "vitepress-plugin-simple-search";
import { defineConfig, searchForWorkspaceRoot } from "vitepress";

export default defineConfig({
    plugins: [SimpleSearch()]
});