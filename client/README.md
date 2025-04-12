# Client Setup

The client is built using the following frameworks:
 [SvelteKit](https://kit.svelte.dev/)
 [ApexCharts](https://apexcharts.com/)
 [Tailwind](https://tailwindcss.com/)
 [TypeScript](https://www.typescriptlang.org/)

## Environment Variables

Before setting up, you will have to create a `.env` file here to store the API keys and other variables

```
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
AUTH_SECRET=
PUBLIC_API_URL=http://127.0.0.1:8000
```


## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.
