import type { TemplateContext } from '../types';

export function generateConfusionProtocol(ctx?: TemplateContext): string {
  return "## Confusion Protocol\n\nWhen evidence conflicts, inspect the relevant source or ask for the missing fact. State material uncertainty and continue work that does not depend on it.";
}
