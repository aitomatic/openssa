/* eslint-disable react/prop-types */
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import styles from "./MarkdownViewer.module.css";

export const MarkdownViewer = ({ children }) => {
  return (
    <ReactMarkdown
      className={styles["content"]}
      // eslint-disable-next-line
      children={children}
      remarkPlugins={[remarkGfm]}
    />
  );
};
