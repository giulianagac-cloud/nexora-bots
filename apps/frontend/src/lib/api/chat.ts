import type { ChatRequestContract, ChatResponseContract } from "@/types/chat";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function chatRequest(
  payload: ChatRequestContract,
): Promise<ChatResponseContract> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: payload.sessionId,
      message: payload.message,
    }),
  });

  if (!response.ok) {
    throw new Error("Unable to reach the HR assistant service.");
  }

  const data = (await response.json()) as {
    session_id: string;
    flow_state: string;
    reply: { id: string; role: "assistant" | "user" | "system"; content: string };
    options: { label: string; keyword: string }[];
  };

  return {
    sessionId: data.session_id,
    flowState: data.flow_state,
    reply: data.reply,
    options: data.options ?? [],
  };
}
