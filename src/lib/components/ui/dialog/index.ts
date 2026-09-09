import { Dialog as DialogPrimitive } from "bits-ui";

import Title from "./dialog-title.svelte";
import Header from "./dialog-header.svelte";
import Overlay from "./dialog-overlay.svelte";
import Content from "./dialog-content.svelte";

const Root = DialogPrimitive.Root;
const Portal = DialogPrimitive.Portal;

export { Root, Title, Portal, Header, Overlay, Content };
