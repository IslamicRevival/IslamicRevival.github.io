import { SearchPlugin } from "vitepress-plugin-search";
import { defineConfig, searchForWorkspaceRoot } from "vitepress";

var options = {
    previewLength: 162,
    buttonLabel: "Search",
    placeholder: "Search docs",
  };

export default defineConfig({
    plugins: [SearchPlugin(options)]
});