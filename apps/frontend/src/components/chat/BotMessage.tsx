import type { ChatOption } from "@/types/chat";

import styles from "./MessageBubble.module.css";

const pdfUrlPattern = /(\/static\/forms\/[^\s]+\.pdf)/g;
const pdfUrlMatcher = /^\/static\/forms\/[^\s]+\.pdf$/;

interface BotMessageProps {
  content: string;
  options?: ChatOption[];
  onOptionClick?: (keyword: string) => void;
}

export function BotMessage({ content, options = [], onOptionClick }: BotMessageProps) {
  const parts = content.split(pdfUrlPattern);

  return (
    <div className={`${styles.row} ${styles.rowAssistant}`}>
      <div>
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
        {options.length > 0 && (
          <div className={styles.options}>
            {options.map((opt) => (
              <button
                key={opt.keyword}
                className={styles.optionButton}
                onClick={() => onOptionClick?.(opt.keyword)}
              >
                {opt.label}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
