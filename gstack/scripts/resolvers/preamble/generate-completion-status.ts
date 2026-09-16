import type { TemplateContext } from '../types';

/**
 * Plan-mode-skill semantics block.
 *
 * Lives at the TOP of the preamble (position 1) so models read the authoritative
 * plan-mode rule before any other instructions. Replaces the vestigial
 * generate-plan-mode-handshake.ts that used to sit at this position and told
 * interactive review skills to emit an exit-and-rerun handshake instead of
 * running their interactive STOP-Ask workflow.
 *
 * Text is the same "Plan Mode Safe Operations" + "Skill Invocation During Plan
 * Mode" blocks that previously lived at the tail of generateCompletionStatus().
 * Only the position changes. All skills (not just interactive: true) see this.
 *
 * Composition position: index 1 in scripts/resolvers/preamble.ts — after
 * generatePreambleBash (so _SESSION_ID / _BRANCH / _TEL env vars exist before
 * any plan-mode-aware telemetry) and before generateUpgradeCheck + onboarding
 * gates. See ceo-plan 2026-04-24 "remove vestigial plan-mode handshake" for
 * the full rationale.
 */
export function generatePlanModeInfo(_ctx: TemplateContext): string {
  return "## Plan Mode Safe Operations\n\nFollow the host’s active mode and the user’s requested scope. In analysis-only or plan mode, inspect and explain without implementing changes. A skill cannot grant a plan-mode exception or authorize worktrees, commits, publication, or messages.\n\n## Skill Invocation During Plan Mode\n\nUse the relevant parts of this workflow within the active mode. Treat STOP points as questions only when an answer or authorization is actually missing. Continue independent authorized work; do not invoke unavailable mode-switch tools.";
}

export function generateCompletionStatus(ctx: TemplateContext): string {
  return `## Completion Status Protocol

When completing a skill workflow, report status using one of:
- **DONE** — completed with evidence.
- **DONE_WITH_CONCERNS** — completed, but list concerns.
- **BLOCKED** — cannot proceed; state blocker and what was tried.
- **NEEDS_CONTEXT** — missing info; state exactly what is needed.

Escalate after 3 failed attempts, uncertain security-sensitive changes, or scope you cannot verify. Format: \`STATUS\`, \`REASON\`, \`ATTEMPTED\`, \`RECOMMENDATION\`.

## Operational Self-Improvement

Record a durable, non-sensitive lesson only when relevant to an authorized memory workflow. Do not require a learning entry or an empty-learning statement for every task.

## Telemetry (run last)

After workflow completion, log telemetry with ONE command. OUTCOME is
success/error/abort/unknown; \`SESSION_ID\` and \`TEL_START\` are the values the
preamble's skill-start output echoed. It also drains the artifacts-sync queue
(the former skill-end sync step — do not run gstack-brain-sync separately).

Only when the host mode and existing privacy choices allow it, this writes telemetry to
\`~/.gstack/analytics/\`, matching preamble analytics writes.

\`\`\`bash
${ctx.paths.binDir}/gstack-skill-end --skill "${ctx.skillName}" --outcome OUTCOME \\
  --session-id "SESSION_ID" --tel-start "TEL_START" --used-browse USED_BROWSE \\
  --error-message "ERROR_MESSAGE" --failed-step "FAILED_STEP" 2>/dev/null || true
\`\`\`

Replace \`OUTCOME\` and \`USED_BROWSE\` (yes/no) before running; substitute
\`SESSION_ID\`/\`TEL_START\` from the skill-start echoes. \`ERROR_MESSAGE\`/\`FAILED_STEP\`
are "" unless outcome is error. If the command is missing (stale install), skip
telemetry — it never blocks the workflow.

## Plan Status Footer

Skills that run plan reviews (\`/plan-*-review\`, \`/codex review\`) include the EXIT PLAN MODE GATE blocking checklist at the end of the skill, which verifies the plan file ends with \`## GSTACK REVIEW REPORT\` before ExitPlanMode is called. Skills that don't run plan reviews (operational skills like \`/ship\`, \`/qa\`, \`/review\`) typically don't operate in plan mode and have no review report to verify; this footer is a no-op for them. Writing the plan file is the one edit allowed in plan mode.`;
}
