---
title: The Box Model
slug: box-model
summary: Understand content, padding, border and margin, and use box-sizing border-box.
minutes: 7
---
## Every element is a box

From the inside out, each box has:

1. **content**: the text or image,
2. **padding**: space inside the border,
3. **border**: the line around it,
4. **margin**: space outside, between this box and others.

```css tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    .box {
      width: 220px;
      padding: 20px;
      border: 4px solid #04AA6D;
      margin: 30px;
      background: #E7F0FF;
    }
  </style>
</head>
<body>
  <div class="box">Padding is the blue area inside the green border. Margin is the empty space outside.</div>
  <div class="box">A second box.</div>
</body>
</html>
```

## Shorthand

`padding` and `margin` take 1 to 4 values, clockwise from the top:

```css
margin: 10px;                /* all sides */
margin: 10px 20px;           /* top+bottom, left+right */
margin: 10px 20px 5px 0;     /* top, right, bottom, left */
margin: 0 auto;              /* centre a box that has a width */
```

## box-sizing

By default `width` is only the content, so padding and border make the box **wider** than you said. `box-sizing: border-box` includes them, which is much easier to work with. Most sites start with:

```css
*, *::before, *::after { box-sizing: border-box; }
```

## block and inline

- **Block** elements (`div`, `p`, `h1`) start on a new line and take the full width.
- **Inline** elements (`span`, `a`, `strong`) sit inside a line; width and height do not apply.
- `display: inline-block` sits in a line but accepts width and height.

## Rounded corners and shadows

```css
.card { border-radius: 12px; box-shadow: 0 4px 12px rgb(0 0 0 / 15%); }
```

## Summary

- Content → padding → border → margin.
- Use `box-sizing: border-box`.
- `margin: 0 auto` centres a box with a width.

```exercise
{
  "title": "A padded card",
  "prompt_md": "Give `.card` a padding of `16px` and a `border-radius` of `8px`.",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n    .card { border: 1px solid #ccc; }\n  </style>\n</head>\n<body>\n  <div class=\"card\">A card</div>\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n    .card { border: 1px solid #ccc; padding: 16px; border-radius: 8px; }\n  </style>\n</head>\n<body>\n  <div class=\"card\">A card</div>\n</body>\n</html>",
  "check_type": "regex",
  "expected_value": "\\.card\\s*\\{(?=[^}]*padding\\s*:\\s*16px)(?=[^}]*border-radius\\s*:\\s*8px)[^}]*\\}",
  "hint": ".card { padding: 16px; border-radius: 8px; }"
}
```

```quiz
[
  {"question": "Which is the space inside the border?", "options": ["padding", "margin", "outline"], "answer": 0, "explanation": "Padding is inside the border; margin is outside."},
  {"question": "What does box-sizing: border-box do?", "options": ["Width includes padding and border", "Adds a border", "Removes the margin"], "answer": 0, "explanation": "The box stays the width you set."}
]
```
