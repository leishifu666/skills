import type { TemplateContext } from '../types';

export function generateSearchBeforeBuildingSection(ctx: TemplateContext): string {
  return "## Search Before Building\n\nInspect relevant existing implementation before adding code. Reuse suitable project or platform facilities. Verify unfamiliar or version-sensitive behavior from current documentation. Do not require a whole-repository survey or learning log for a small change.";
}

