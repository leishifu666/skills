import type { TemplateContext } from '../types';

export function generateCompletenessSection(ctx?: TemplateContext): string {
  return "## Completeness Principle — Boil the Ocean\n\nComplete the requested outcome and relevant verification. Scope completeness to the user’s goal; do not add unrelated features, audits, dependencies, or delivery stages.";
}
