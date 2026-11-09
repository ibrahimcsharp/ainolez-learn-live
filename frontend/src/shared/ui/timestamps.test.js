import { afterEach, expect, test } from "vitest";
import { enableTimestampLinks, playerBefore, secondsOf, seekFromAddress } from "./timestamps";

afterEach(() => {
  document.body.innerHTML = "";
});

test("reads the seconds from a timestamp address", () => {
  expect(secondsOf("https://www.youtube.com/watch?v=abc&t=40s")).toBe(40);
  expect(secondsOf("https://vimeo.com/123#t=75s")).toBe(75);
  expect(secondsOf("#t=10")).toBe(10);
  expect(secondsOf("https://example.com/")).toBeNull();
});

test("a click moves the video above to that moment instead of leaving the page", () => {
  enableTimestampLinks();
  document.body.innerHTML = `
    <iframe id="runner" src="https://api.ainolez.com/runner/"></iframe>
    <iframe id="video" src="https://www.youtube-nocookie.com/embed/abc?start=0" allow="encrypted-media"></iframe>
    <a class="timestamp" href="https://www.youtube.com/watch?v=abc&amp;t=40s">00:40</a>
    <iframe id="later" src="https://www.youtube-nocookie.com/embed/xyz"></iframe>`;
  const link = document.querySelector("a.timestamp");
  expect(playerBefore(link).id).toBe("video");

  const event = new MouseEvent("click", { bubbles: true, cancelable: true, button: 0 });
  link.dispatchEvent(event);
  const video = document.getElementById("video");
  expect(event.defaultPrevented).toBe(true);
  expect(video.src).toContain("start=40");
  expect(video.src).toContain("autoplay=1");
  expect(video.allow).toContain("autoplay");
});

test("without a video above, the link works as a normal link", () => {
  document.body.innerHTML = `<a class="timestamp" href="https://www.youtube.com/watch?v=abc&amp;t=40s">00:40</a>`;
  expect(playerBefore(document.querySelector("a"))).toBeNull();
});

test("an address with ?t=40 starts the page's video at 0:40 once it appears", async () => {
  seekFromAddress("?t=40");
  document.body.innerHTML = `<div class="lesson-content">
    <iframe src="https://www.youtube-nocookie.com/embed/abc?start=0"></iframe></div>`;
  await new Promise((resolve) => setTimeout(resolve, 0));
  expect(document.querySelector("iframe").src).toContain("start=40");
});
