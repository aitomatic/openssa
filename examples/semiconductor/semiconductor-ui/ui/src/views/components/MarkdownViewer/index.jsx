/* eslint-disable react/prop-types */
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

// Import KaTeX CSS for styling
import "katex/dist/katex.min.css";

import styles from "./MarkdownViewer.module.css";

function preprocessMarkdown(markdown) {
  return (
    markdown
      // Replace LaTeX display math delimiters \[ and \] with $$
      .replace(/\\\[/g, "$$")
      .replace(/\\\]/g, "$$")
    // Escape backslashes in LaTeX expressions
    // .replace(/(\\text|\\frac|\\{|\\})/g, "\\$&")
    // Escape backslashes globally
    // .replace(/\\/g, "\\\\")
    // Escape dollar signs outside LaTeX (optional, if needed)
    // .replace(/(?<!\\)\$(?!\$)/g, "\\$")
  );
}

const markdown = `
$$
\\text{Dry tons biosolids/acre} = \\frac{\\text{Adjusted N rate (lbs N/acre)}}{\\text{PAN (lbs N/ton)}}
$$
`;

export const MarkdownViewer = ({ children }) => {
  const content = preprocessMarkdown(children);
  console.log({
    content,
    children,
  });
  return (
    <ReactMarkdown
      className={styles["content"]}
      // eslint-disable-next-line
      children={content}
      remarkPlugins={[remarkGfm, remarkMath]}
      rehypePlugins={[rehypeKatex]}
    />
  );
};
