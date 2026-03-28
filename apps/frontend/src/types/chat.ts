export type ChatRole = "assistant" | "user" | "system";

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
}

export interface ChatOption {
  label: string;
  keyword: string;
}

export interface ChatRequestContract {
  sessionId: string;
  message: string;
}

export interface ChatResponseContract {
  sessionId: string;
  flowState: string;
  reply: ChatMessage;
  options: ChatOption[];
}
