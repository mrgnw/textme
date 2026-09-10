import { MediaQuery } from "svelte/reactivity";

export const isMobile = new MediaQuery("(max-width: 640px)");
export const isWide = new MediaQuery("(min-width: 1024px)");
