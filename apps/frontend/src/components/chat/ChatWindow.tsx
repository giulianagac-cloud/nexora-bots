import type { ChatMessage } from "@/types/chat";

import { BotMessage } from "./BotMessage";
import { ChatInput } from "./ChatInput";
import { EmptyState } from "./EmptyState";
import { LoadingState } from "./LoadingState";
import { UserMessage } from "./UserMessage";
import styles from "./ChatWindow.module.css";

interface ChatWindowProps {
  botName: string;
  messages: ChatMessage[];
  isLoading?: boolean;
  error?: string | null;
  onSendMessage: (value: string) => Promise<void> | void;
}

export function ChatWindow({
  botName,
  messages,
  isLoading = false,
  error,
  onSendMessage,
}: ChatWindowProps) {
  const isEmpty = messages.length === 0;

  return (
    <div className={styles.frame}>
      <header className={styles.header}>
        <div className={styles.avatar}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
          </svg>
        </div>

        <div className={styles.headerInfo}>
          <p className={styles.headerName}>{botName}</p>
          <div className={styles.headerStatus}>
            <span className={styles.statusDot} />
            <span className={styles.statusText}>En línea</span>
          </div>
        </div>

        <span className={styles.headerBrand}>nexora</span>
      </header>

      <div className={styles.body} data-empty={isEmpty}>
        {isEmpty ? <EmptyState /> : null}
        {messages.map((message) =>
          message.role === "user" ? (
            <UserMessage key={message.id} content={message.content} />
          ) : (
            <BotMessage key={message.id} content={message.content} />
          ),
        )}
        {isLoading ? <LoadingState /> : null}
        {error ? <div className={styles.error}>{error}</div> : null}
      </div>

      <footer className={styles.footer}>
        <ChatInput disabled={isLoading} onSend={onSendMessage} />
      </footer>
    </div>
  );
}
