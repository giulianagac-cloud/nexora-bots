"use client";

import { useEffect, useState, useTransition } from "react";

import { ChatWindow } from "@/components/chat/ChatWindow";
import { chatRequest } from "@/lib/api/chat";
import { fetchBotConfig } from "@/lib/api/config";
import { ensureMocks } from "@/lib/mocks";
import type { ChatMessage, ChatOption } from "@/types/chat";

import styles from "./page.module.css";

export default function HomePage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [options, setOptions] = useState<ChatOption[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isSending, setIsSending] = useState(false);
  const [isPending, startTransition] = useTransition();
  const [isReady, setIsReady] = useState(false);
  const [botName, setBotName] = useState("Asistente");

  useEffect(() => {
    Promise.all([
      ensureMocks(),
      fetchBotConfig().then((cfg) => setBotName(cfg.bot_name)).catch(() => {}),
    ]).finally(() => setIsReady(true));
  }, []);

  useEffect(() => {
    if (!isReady) return;
    triggerWelcome();
  }, [isReady]);

  async function triggerWelcome() {
    setIsSending(true);
    try {
      const response = await chatRequest({
        sessionId: "demo-session",
        message: "__init__",
      });
      startTransition(() => {
        setMessages([
          {
            id: response.reply.id,
            role: response.reply.role,
            content: response.reply.content,
          },
        ]);
        setOptions(response.options);
      });
    } catch {
      // silencioso — el usuario verá el chat vacío
    } finally {
      setIsSending(false);
    }
  }

  async function handleSendMessage(value: string) {
    setError(null);
    setIsSending(true);
    setOptions([]);

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
        setOptions(response.options);
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
          options={options}
          onSendMessage={handleSendMessage}
        />
      </div>
    </main>
  );
}
