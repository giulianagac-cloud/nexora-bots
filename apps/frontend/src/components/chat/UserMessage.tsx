import styles from "./MessageBubble.module.css";

export function UserMessage({ content }: { content: string }) {
  return (
    <div className={`${styles.row} ${styles.rowUser}`}>
      <div>
        <div className={`${styles.label} ${styles.labelUser}`}>You</div>
        <div className={`${styles.bubble} ${styles.bubbleUser}`}>{content}</div>
      </div>
    </div>
  );
}

