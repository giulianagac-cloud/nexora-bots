"use client";

import { FormEvent, useState } from "react";

import styles from "./ChatInput.module.css";

interface ChatInputProps {
  disabled?: boolean;
  onSend: (value: string) => Promise<void> | void;
}

export function ChatInput({ disabled = false, onSend }: ChatInputProps) {
  const [value, setValue] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = value.trim();
    if (!trimmed) {
      return;
    }

    setValue("");
    await onSend(trimmed);
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <input
        className={styles.input}
        disabled={disabled}
        onChange={(event) => setValue(event.target.value)}
        placeholder="Escribí tu consulta..."
        value={value}
      />
      <button className={styles.button} disabled={disabled} type="submit">
        Enviar
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M5 12h14M12 5l7 7-7 7" />
        </svg>
      </button>
    </form>
  );
}
