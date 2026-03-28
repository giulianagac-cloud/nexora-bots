import styles from "./MessageBubble.module.css";

export function UserMessage({ content }: { content: string }) {
  return (
    <div className={`${styles.row} ${styles.rowUser}`}>
      <div className={`${styles.bubble} ${styles.bubbleUser}`}>{content}</div>
    </div>
  );
}
