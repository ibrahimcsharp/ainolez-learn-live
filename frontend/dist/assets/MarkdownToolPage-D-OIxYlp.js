import{r as n,j as e}from"./index-BFFJ9wUl.js";import{u as i}from"./useMarkdownPreview-CEIyYpXt.js";import{s as o}from"./admin.module-BXkYcN3R.js";import{C as l}from"./copy-CzHmnafl.js";const c=`## Hello ainolez

Write **Markdown** on the left and see the result on the right.

!!! tip
    Put a video on its own line with \`{{youtube:VIDEO_ID}}\`, \`{{vimeo:VIDEO_ID}}\`
    or \`{{video:https://example.com/clip.mp4}}\`.
`;function h(){const[t,r]=n.useState(c),s=i(t);return e.jsxs(e.Fragment,{children:[e.jsxs("div",{className:o.toolbar,children:[e.jsx("h1",{children:"Markdown converter"}),e.jsxs("button",{className:"btn btn-outline",onClick:()=>navigator.clipboard.writeText(s),children:[e.jsx(l,{})," Copy HTML"]})]}),e.jsx("p",{className:"muted",children:"To turn .md files into lessons, open a course and use “Import Markdown” on a chapter."}),e.jsxs("div",{className:o.split,children:[e.jsx("textarea",{className:`${o.code} ${o.preview}`,rows:24,value:t,onChange:a=>r(a.target.value),"aria-label":"Markdown"}),e.jsx("div",{className:`lesson-content ${o.preview}`,dangerouslySetInnerHTML:{__html:s}})]})]})}export{h as MarkdownToolPage};
