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
        placeholder="Ask about leave, payroll, certificates..."
        value={value}
      />
      <button className={styles.button} disabled={disabled} type="submit">
        Send
      </button>
    </form>
  );
}

