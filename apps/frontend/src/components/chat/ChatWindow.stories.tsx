import type { Meta, StoryObj } from "@storybook/react";

import { ChatWindow } from "./ChatWindow";

const meta = {
  title: "Chat/ChatWindow",
  component: ChatWindow,
  parameters: {
    layout: "centered",
  },
  args: {
    botName: "Asistente Nexora",
    options: [],
    onSendMessage: async () => {},
  },
} satisfies Meta<typeof ChatWindow>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    messages: [
      {
        id: "assistant-1",
        role: "assistant",
        content: "¡Hola! Soy el asistente de Nexora. ¿En qué puedo ayudarte hoy?",
      },
      {
        id: "user-1",
        role: "user",
        content: "Quiero sacar un turno.",
      },
      {
        id: "assistant-2",
        role: "assistant",
        content: "Para sacar un turno podés contactarnos por WhatsApp o email.",
      },
    ],
  },
};

export const WithOptions: Story = {
  args: {
    messages: [
      {
        id: "assistant-1",
        role: "assistant",
        content: "¡Hola! Soy el asistente de Nexora. ¿En qué puedo ayudarte hoy?",
      },
    ],
    options: [
      { label: "Quiero sacar un turno", keyword: "turno" },
      { label: "Consultar precios", keyword: "precio" },
      { label: "Hablar con alguien", keyword: "contacto" },
    ],
  },
};

export const Empty: Story = {
  args: {
    messages: [],
  },
};

export const Loading: Story = {
  args: {
    isLoading: true,
    messages: [
      {
        id: "assistant-1",
        role: "assistant",
        content: "¡Hola! Soy el asistente de Nexora. ¿En qué puedo ayudarte hoy?",
      },
    ],
  },
};

export const Error: Story = {
  args: {
    error: "El asistente no está disponible en este momento.",
    messages: [
      {
        id: "assistant-1",
        role: "assistant",
        content: "Por favor intentá de nuevo.",
      },
    ],
  },
};
