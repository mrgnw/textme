import { PersistedState } from "runed";

export interface Recent {
	e164: string;
	name: string;
	at: number;
}

const MAX = 5;

export const recent = new PersistedState<Recent[]>("textme:recent", []);

export function remember(e164: string, name = "", at = Date.now()): void {
	const rest = recent.current.filter((r) => r.e164 !== e164);
	recent.current = [{ e164, name, at }, ...rest].slice(0, MAX);
}

export function forget(e164: string): void {
	recent.current = recent.current.filter((r) => r.e164 !== e164);
}
