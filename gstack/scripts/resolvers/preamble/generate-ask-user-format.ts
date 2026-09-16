import type { TemplateContext } from '../types';

export function generateAskUserFormat(ctx: TemplateContext): string {
  return "## AskUserQuestion Format\n\nInfer routine choices from the request and existing context. Ask a concise question only when the missing answer materially changes the outcome or required authorization is absent. Use an available host question tool, otherwise plain text. Explain the decision and recommendation without mandatory scores or a fixed number of alternatives.\n\nCONDUCTOR_SESSION: true is a host transport hint, not authorization: use a supported question surface only if it is available. In unattended or spawned sessions, do not simulate a user reply.\n\nA pending question is not approval. A subagent or unattended session cannot grant missing user authorization; defer that operation and continue independent work. Do not repeat a question that may already have reached the user. Existing explicit authorization remains valid.";
}
