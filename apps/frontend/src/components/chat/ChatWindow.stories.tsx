import type { Meta, StoryObj } from "@storybook/react";

import { ChatWindow } from "./ChatWindow";

const meta = {
  title: "Chat/ChatWindow",
  component: ChatWindow,
  parameters: {
    layout: "centered",
  },
  args: {
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
        content: "Hello. I can help you navigate common HR procedures.",
      },
      {
        id: "user-1",
        role: "user",
        content: "I need help with vacation time.",
      },
      {
        id: "assistant-2",
        role: "assistant",
        content: "Tell me whether the request is planned leave or an urgent absence.",
      },
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
        content: "I can prepare the next step in your leave process.",
      },
    ],
  },
};

export const Error: Story = {
  args: {
    error: "Unable to reach the HR assistant service.",
    messages: [
      {
        id: "assistant-1",
        role: "assistant",
        content: "Please try your request again.",
      },
    ],
  },
};

