const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function fetchBotConfig(): Promise<{ bot_name: string }> {
  const response = await fetch(`${API_BASE_URL}/config`);
  if (!response.ok) {
    throw new Error("Unable to fetch bot config.");
  }
  return response.json() as Promise<{ bot_name: string }>;
}
