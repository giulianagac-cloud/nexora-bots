import type { Meta, StoryObj } from "@storybook/react";

import { ChatInput } from "./ChatInput";

const meta = {
  title: "Chat/ChatInput",
  component: ChatInput,
  args: {
    onSend: async () => {},
  },
} satisfies Meta<typeof ChatInput>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const Disabled: Story = {
  args: {
    disabled: true,
  },
};

