# Frontend

Next.js App Router frontend for the TrenBot Enterprise internal HR assistant demo.

## Run

```bash
npm install
npm run msw:init
npm run dev
```

To enable browser-level API mocking during development:

```bash
NEXT_PUBLIC_API_MOCKING=enabled npm run dev
```

## Storybook

```bash
npm run storybook
```

## Notes

- `npm run msw:init` generates `public/mockServiceWorker.js`.
- Stories are available for the main chat components and UI states.
