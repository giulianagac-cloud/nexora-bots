import type { Meta, StoryObj } from "@storybook/react";

import { EmptyState } from "./EmptyState";
import { ErrorState } from "./ErrorState";
import { LoadingState } from "./LoadingState";

const meta = {
  title: "Chat/States",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Empty: Story = {
  render: () => <EmptyState />,
};

export const Loading: Story = {
  render: () => <LoadingState />,
};

export const Error: Story = {
  render: () => <ErrorState />,
};

