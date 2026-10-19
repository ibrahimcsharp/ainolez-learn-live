---
title: Links and Images
slug: links-images
summary: Link pages together with <a> and add images with <img> and good alt text.
minutes: 7
---
## Links

The `<a>` (anchor) element makes a link. The `href` attribute says where it goes:

```html tryit
<!DOCTYPE html>
<html lang="en">
<body>
  <p><a href="https://developer.mozilla.org">MDN Web Docs</a> is a great reference.</p>
  <p><a href="https://en.wikipedia.org" target="_blank" rel="noopener">Wikipedia</a> opens in a new tab.</p>
  <p><a href="mailto:hello@example.com">Email us</a></p>
  <p><a href="#contact">Jump to the contact section</a></p>
</body>
</html>
```

- A full URL (`https://...`) links to another site.
- A relative path (`about.html`, `/courses`) links to a page on the same site.
- `#contact` jumps to the element with `id="contact"` on the same page.
- `target="_blank"` opens a new tab; add `rel="noopener"` for safety.

Write link text that says where the link goes. "Read the pricing guide" is better than "click here".

## Images

`<img>` shows an image. It has no closing tag.

```html tryit
<!DOCTYPE html>
<html lang="en">
<body>
  <img src="https://picsum.photos/id/1025/400/260"
       alt="A pug wrapped in a blanket"
       width="400" height="260">
</body>
</html>
```

- `src` is the image address.
- `alt` describes the image for people who cannot see it and for search engines. It also shows if the image fails to load.
- `width` and `height` let the browser keep space for the image while it loads.

## An image as a link

Put the `<img>` inside an `<a>`:

```html
<a href="/courses"><img src="logo.png" alt="ainolez home"></a>
```

## Summary

- `<a href="...">` makes a link; the text inside is what people click.
- `<img src="..." alt="...">` shows an image; always write useful alt text.

```exercise
{
  "title": "Link to the docs",
  "prompt_md": "Turn the text `MDN` into a link to `https://developer.mozilla.org`.",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n  <p>Look things up on MDN.</p>\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n  <p>Look things up on <a href=\"https://developer.mozilla.org\">MDN</a>.</p>\n</body>\n</html>",
  "check_type": "regex",
  "expected_value": "<a\\s+href=[\"']https://developer\\.mozilla\\.org/?[\"']\\s*>\\s*MDN\\s*</a>",
  "hint": "<a href=\"https://developer.mozilla.org\">MDN</a>"
}
```

```quiz
[
  {"question": "Which attribute sets where a link goes?", "options": ["href", "src", "alt"], "answer": 0, "explanation": "href is the link's destination; src is an image's address."},
  {"question": "Why does an image need alt text?", "options": ["It describes the image for people who cannot see it", "It makes the image larger", "It is required for the image to load"], "answer": 0, "explanation": "Screen readers read alt text aloud, and search engines use it."}
]
```
