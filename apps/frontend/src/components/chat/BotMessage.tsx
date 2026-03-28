import styles from "./MessageBubble.module.css";

const pdfUrlPattern = /(\/static\/forms\/[^\s]+\.pdf)/g;
const pdfUrlMatcher = /^\/static\/forms\/[^\s]+\.pdf$/;

export function BotMessage({ content }: { content: string }) {
  const parts = content.split(pdfUrlPattern);

  return (
    <div className={`${styles.row} ${styles.rowAssistant}`}>
      <div className={`${styles.bubble} ${styles.bubbleAssistant}`}>
        {parts.map((part, index) =>
          pdfUrlMatcher.test(part) ? (
            <a key={`${part}-${index}`} href={`http://127.0.0.1:8001${part}`}>
              {part}
            </a>
          ) : (
            part
          ),
        )}
      </div>
    </div>
  );
}
