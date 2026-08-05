import { EditorView, basicSetup } from "codemirror";
import { javascript } from "@codemirror/lang-javascript";
import { oneDark } from "@codemirror/theme-one-dark";

const DEFAULT_SOURCE = `// Project Nexus — Frontier Syntax (preview)
fn main() {
  print("Hello from Nexus IDE");
}
`;

const statusEl = document.getElementById("status");
const runBtn = document.getElementById("run-btn");

const view = new EditorView({
  doc: DEFAULT_SOURCE,
  extensions: [basicSetup, javascript(), oneDark, EditorView.lineWrapping],
  parent: document.getElementById("editor"),
});

async function runFrontier() {
  statusEl.textContent = "Running…";
  try {
    const { invoke } = await import("@tauri-apps/api/core");
    const source = view.state.doc.toString();
    const result = await invoke("run_frontier", { source });
    statusEl.textContent = String(result);
  } catch (err) {
    statusEl.textContent = `Browser mode: ${view.state.doc.length} chars`;
    console.info("Tauri invoke unavailable outside desktop shell", err);
  }
}

runBtn.addEventListener("click", runFrontier);
statusEl.textContent = "Ready — 60+ FPS UI target";
