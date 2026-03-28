"use client";

import { useEffect, useState, useTransition } from "react";

import { ChatWindow } from "@/components/chat/ChatWindow";
import { chatRequest } from "@/lib/api/chat";
import { fetchBotConfig } from "@/lib/api/config";
import { ensureMocks } from "@/lib/mocks";
import type { ChatMessage } from "@/types/chat";

import styles from "./page.module.css";

const initialMessages: ChatMessage[] = [
  {
    id: "welcome",
    role: "assistant",
    content: "¡Hola! Soy el asistente de Nexora. ¿En qué puedo ayudarte hoy?",
  },
];

export default function HomePage() {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [error, setError] = useState<string | null>(null);
  const [isSending, setIsSending] = useState(false);
  const [isPending, startTransition] = useTransition();
  const [isReady, setIsReady] = useState(false);
  const [botName, setBotName] = useState("Asistente");

  useEffect(() => {
    ensureMocks().finally(() => setIsReady(true));
    fetchBotConfig()
      .then((cfg) => setBotName(cfg.bot_name))
      .catch(() => {});
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
          : "El asistente no está disponible en este momento.",
      );
    } finally {
      setIsSending(false);
    }
  }

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <ChatWindow
          botName={botName}
          error={error}
          isLoading={isSending || isPending || !isReady}
          messages={messages}
          onSendMessage={handleSendMessage}
        />
      </div>
    </main>
  );
}
