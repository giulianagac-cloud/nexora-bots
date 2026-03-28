import { delay, http, HttpResponse } from "msw";

const defaultReply = {
  session_id: "demo-session",
  flow_state: "intake",
  reply: {
    id: "assistant-default",
    role: "assistant" as const,
    content:
      "I can help with leave, payroll, certificates, and employee processes. Tell me what you need.",
  },
};

export const handlers = [
  http.post("http://127.0.0.1:8000/chat", async ({ request }) => {
    const body = (await request.json()) as { message?: string; session_id?: string };
    const normalized = body.message?.toLowerCase() ?? "";

    if (normalized.includes("delay")) {
      await delay(1800);
      return HttpResponse.json({
        session_id: body.session_id ?? "demo-session",
        flow_state: "delayed_response",
        reply: {
          id: "assistant-delay",
          role: "assistant",
          content: "This mocked response simulates a slower backend reply for UI testing.",
        },
      });
    }

    if (normalized.includes("error")) {
      return new HttpResponse(null, { status: 500 });
    }

    if (normalized.includes("vacation") || normalized.includes("leave")) {
      return HttpResponse.json({
        session_id: body.session_id ?? "demo-session",
        flow_state: "leave_guidance",
        reply: {
          id: "assistant-leave",
          role: "assistant",
          content:
            "To begin a leave request, tell me the absence type and your expected dates. I can guide the next steps.",
        },
      });
    }

    return HttpResponse.json(defaultReply);
  }),
];

