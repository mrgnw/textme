import { links, shareUrl, type App } from "./phone";

export type Channel = App | "link";

export const CHANNELS: Record<Channel, { label: string; fill: string; line: string; color: string }> = {
	link: { label: "textme", fill: "bg-primary text-primary-foreground", line: "border-primary-foreground/30", color: "text-primary" },
	telegram: { label: "Telegram", fill: "bg-telegram text-telegram-foreground", line: "border-telegram-foreground/30", color: "text-telegram" },
	whatsapp: { label: "WhatsApp", fill: "bg-whatsapp text-whatsapp-foreground", line: "border-whatsapp-foreground/30", color: "text-whatsapp" },
	sms: { label: "SMS", fill: "bg-sms text-sms-foreground", line: "border-sms-foreground/30", color: "text-sms" },
};

export const CHANNEL_ORDER: Channel[] = ["link", "telegram", "whatsapp", "sms"];

export function channelUrl(origin: string, e164: string, channel: Channel): string {
	return channel === "link" ? shareUrl(origin, e164) : links(e164)[channel];
}

export function shownUrl(url: string): string {
	return url.replace(/^https?:\/\//, "");
}
