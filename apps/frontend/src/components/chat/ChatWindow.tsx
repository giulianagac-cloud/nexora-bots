import type { ChatMessage } from "@/types/chat";

import { BotMessage } from "./BotMessage";
import { ChatInput } from "./ChatInput";
import { EmptyState } from "./EmptyState";
import { LoadingState } from "./LoadingState";
import { UserMessage } from "./UserMessage";
import styles from "./ChatWindow.module.css";

interface ChatWindowProps {
  messages: ChatMessage[];
  isLoading?: boolean;
  error?: string | null;
  onSendMessage: (value: string) => Promise<void> | void;
}

export function ChatWindow({
  messages,
  isLoading = false,
  error,
  onSendMessage,
}: ChatWindowProps) {
  const isEmpty = messages.length === 0;

  return (
    <div className={styles.frame}>
      <header className={styles.header}>
        <div>
          <h2 className={styles.headerTitle}>HR Assistant</h2>
          <p className={styles.headerSubtitle}>Employee guidance for common internal requests</p>
        </div>
        <div className={styles.status}>{isLoading ? "Processing" : "Available"}</div>
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

