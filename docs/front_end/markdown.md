---
layout: default
title: Markdown Magic
parent: Frontend Stuff
permalink: /frontend-stuff/markdown
---

# Markdown Magic
All the little things in markdown that we often forget...

## Collapsable sections in markdown

This gist is helpful for github.com and gist.github.com specifically:
[markdown-details-collapsible.md](https://gist.github.com/pierrejoubert73/902cc94d79424356a8d20be2b382e1ab)

But the above doesn't work on my jekyll based github pages docs, so I found this:
[Jekyll Text Expand or Collapsible Markdown](https://www.tomordonez.com/jekyll-text-expand-collapsible-markdown/)

### Working Example

And that didn't work either 🙃 which was frustrating, so then I found this repo:
[github/jekyll-commonmark-ghpages](https://github.com/github/jekyll-commonmark-ghpages#installation)

and the answer was this being added to my `_config.yml` for my jekyll site:

```yaml
markdown: CommonMarkGhPages
commonmark:
  options: ["UNSAFE", "SMART", "FOOTNOTES"]
  extensions: ["strikethrough", "autolink", "table", "tagfilter"]
```

Then at last this worked in my markdown file:

<details>
  <summary>Python3.12</summary>

  Check out this bash syntax highlighted block:

  ```bash
    brew install python@3.12
  ```

</details>

Markdown for the above example:

```markdown
  <details>
    <summary>Python3.12</summary>

    Below, you can change the first ``` to ```bash for syntax highlighting :)
    Checkout this regular code block:

    ```
    brew install python@3.12
    ```

  </details>
```

Sources to this page specifically if you want to look at the raw:

- [docs/front_end/markdown.md on github.com](https://github.com/jessebot/onboardme/blob/main/docs/front_end/markdown.md)
- [RAW docs/front_end/markdown.md](https://raw.githubusercontent.com/jessebot/onboardme/main/docs/front_end/markdown.md)
- [`_config.yml`](https://github.com/jessebot/onboardme/blob/main/docs/_config.yml#L17).
- Finally, the link to [this jekyll page](https://jessebot.github.io/onboardme/frontend-stuff/markdown).
