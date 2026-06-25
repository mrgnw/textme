import { defineConfig, devices } from "@playwright/test";

const PORT = 4319;

export default defineConfig({
	testDir: "tests",
	fullyParallel: true,
	use: {
		baseURL: `http://localhost:${PORT}`,
	},
	projects: [
		{ name: "chromium", use: { ...devices["Desktop Chrome"] } },
	],
	webServer: {
		command: `pnpm build && pnpm preview --port ${PORT} --strictPort`,
		port: PORT,
		reuseExistingServer: !process.env.CI,
		timeout: 120_000,
	},
});
