import { describe, expect, it } from "vitest";
import { isWholeDocument, pageDocument, tabForFile } from "./codePage";

describe("pageDocument", () => {
  it("wraps a fragment and puts the CSS in the head and the JS after the HTML", () => {
    const html = pageDocument({ title: "A <b>", html: "<h1>Hi</h1>", css: "h1{color:red}", js: "go('</script>')" });
    expect(html.startsWith("<!doctype html>")).toBe(true);
    expect(html).toContain("<title>A &lt;b></title>");
    expect(html.indexOf("<style>h1{color:red}</style>")).toBeLessThan(html.indexOf("</head>"));
    expect(html).toContain("<h1>Hi</h1><script>go('<\\/script>')</script></body>");
  });

  it("keeps a whole document as written", () => {
    const whole = "<!DOCTYPE html><html><head><title>X</title></head><body><p>Hi</p></body></html>";
    const html = pageDocument({ html: whole, js: "go()" });
    expect(isWholeDocument(whole)).toBe(true);
    expect(html.startsWith("<!DOCTYPE html><html><head><title>X</title>")).toBe(true);
    expect(html.endsWith("<p>Hi</p><script>go()</script></body></html>")).toBe(true);
  });
});

it("sends imported files to the right tab", () => {
  expect(tabForFile("Index.HTML")).toBe("code_html");
  expect(tabForFile("site.css")).toBe("code_css");
  expect(tabForFile("app.js")).toBe("code_js");
  expect(tabForFile("logo.png")).toBe(null);
});
