---
title: How to add or update content
---

# How to add or update content

We want everyone to share & archive books, articles, documents, pdfs, videos files on various Islaamic sciences as we are a non-partisan, non-sectarian site.    

Contribute Islamic knowledge freely using coding techniques of peer-reviewing and versioning

## Technology

The Islamic Revival framework is powered by Vitepress, VueJS, ChatGPT (Darwin AI NLP), custom python code, YouTube APIs and various other opensource packages for performant content, administration and searching.

It uses Markdown in the `/content/` folder to render every document. If you don't know what Markdown is (or need a refresher), take a minute to look over [the basics][1].

## Adding Articles

All articles are stored as Markdown files under [`/content/`][2]. 

To create a new article, you need to be logged into GitHub with your personal username, then click the "Add file" dropdown menu near the top right of the [`/content/`][2] page.

Name the file something short but descriptive as it will become part of the URL, for
example `opnions-on-salah.md` - don't use spaces; instead,
use dashes (`-`).

Then include the following text at the very top of the file (including the
`---`es).

```yaml
---
title: Opinions on salah
description: >
  A more descriptive sentence or two about the page; will show up in search
  engines and on the home page.
keywords:
  - List
  - of
  - keywords
  - about
  - this
  - page

facebookImage: /_social/article
twitterImage: /_social/article
---
```

A couple of notes:

- After the `---` line, you can type the contents of the article in markdown.
Feel free to use `# Heading1`, `## Heading2`, `**bold**`, `_italic_`, and other
markdown to make the page look awesome.

- For keyboard shortcuts, use the HTML tag `<kbd>`, i.e.
`<kbd>Alt</kbd>+<kbd>F4</kbd>`.

When you're all done, fill out the "Commit new file" form at the bottom with the
description of your changes and press the "Commit changes" button.

## Editing an Article

To edit or update an article, click on the article's file in [GitHub][2]. Then
click the pencil "Edit this file" icon on the top-right. You can now edit the
contents right in GitHub. To see what it will look like before you save it,
click the "Preview changes" tab at the top.

When you're all done, fill out the "Commit changes" form at the bottom with the
description of your changes and press the "Commit changes" button. This will generate a Pull Request for an admin to review.

## Beautifying Markdown content
To beautify markdown content, you can use a markdown editor or previewer that supports formatting options such as headings, bold and italic text, lists, links, and images. Some examples of markdown editors and previewers include Typora, Dillinger, and StackEdit.

To use these tools, simply open the editor or previewer and paste your markdown content into the editor window. The editor or previewer will automatically format the content according to the markdown syntax, making it easier to read and understand.

You can also use markdown extensions or plugins for your text editor or word processor to add markdown formatting options directly within the editor. For example, if you use Microsoft Word, you can install the Markdown Monster extension to add markdown formatting options to the editor.

Additionally, there are online markdown tools that allow you to convert markdown content into HTML or PDF format, which can be useful for sharing your content with others or for publishing it on the web. Some examples of online markdown converters include Markdown to HTML and Markdown to PDF.

Overall, using a markdown editor or previewer, along with extensions and online tools, can help make your markdown content more readable and visually appealing.

## Files, Images, and Links

To store files, put them in the `/content/public` folder. 

Anything in that folder will be available at the base URL. 

When linking to files, please use the absolute path, i.e.
`/images/islam.png`.


## Local Development

For simple edits, you can directly edit the file on GitHub and generate a Pull Request per above, else you will need to clone this repository to your local computer.


## Project setup

```
git clone https://github.com/IslamicRevival/IslamicRevival.github.io.git

yarn install
```

### Compiles and hot-reloads for development

```
# yarn
yarn dev
```

### Compiles and minifies for production

```
# yarn
yarn build
```


[1]: https://help.github.com/articles/markdown-basics/
[2]: https://github.com/IslamicRevival/IslamicRevival.github.io/tree/main/content

