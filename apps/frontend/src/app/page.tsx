"use client";

import { useEffect, useState, useTransition } from "react";

import { ChatWindow } from "@/components/chat/ChatWindow";
import { chatRequest } from "@/lib/api/chat";
import { ensureMocks } from "@/lib/mocks";
import type { ChatMessage } from "@/types/chat";

import styles from "./page.module.css";

const initialMessages: ChatMessage[] = [
  {
    id: "welcome",
    role: "assistant",
    content:
      "Welcome to TrenBot Enterprise. I can guide you through common HR requests such as leave, payroll, and employee documents.",
  },
];

export default function HomePage() {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [error, setError] = useState<string | null>(null);
  const [isSending, setIsSending] = useState(false);
  const [isPending, startTransition] = useTransition();
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    ensureMocks().finally(() => setIsReady(true));
  }, []);

  async function handleSendMessage(value: string) {
    setError(null);
    setIsSending(true);

    const outgoing: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: value,
    };

    setMessages((current) => [...current, outgoing]);

    try {
      const response = await chatRequest({
        sessionId: "demo-session",
        message: value,
      });

      startTransition(() => {
        setMessages((current) => [
          ...current,
          {
            id: response.reply.id,
            role: response.reply.role,
            content: response.reply.content,
          },
        ]);
      });
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "The assistant is temporarily unavailable.",
      );
    } finally {
      setIsSending(false);
    }
  }

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <section className={styles.heroCard}>
          <p className={styles.eyebrow}>Internal Employee Experience</p>
          <div className={styles.titleRow}>
            <h1 className={styles.title}>TrenBot Enterprise</h1>
            <div className={styles.badge}>
              <span className={styles.badgeDot} />
              Demo-ready HR assistant
            </div>
          </div>
          <p className={styles.subtitle}>
            A mobile-first assistant concept for Trenes employees, built to support guided HR
            flows today and future enterprise integrations tomorrow.
          </p>
        </section>

        <section className={styles.chatArea}>
          <ChatWindow
            error={error}
            isLoading={isSending || isPending || !isReady}
            messages={messages}
            onSendMessage={handleSendMessage}
          />
        </section>
      </div>
    </main>
  );
}
