import type { Meta, StoryObj } from "@storybook/react";

import { BotMessage } from "./BotMessage";
import { UserMessage } from "./UserMessage";

const meta = {
  title: "Chat/Messages",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const User: Story = {
  render: () => <UserMessage content="I need my latest payroll receipt." />,
};

export const Bot: Story = {
  render: () => (
    <BotMessage content="I can guide you to the payroll documents flow and the expected publication date." />
  ),
};

