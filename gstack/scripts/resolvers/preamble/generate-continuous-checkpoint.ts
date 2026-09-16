

export function generateContinuousCheckpoint(): string {
  return "## Continuous Checkpoint Mode\n\nFor long tasks, preserve the goal, completed work, evidence, and remaining work when context loss is likely. Do not create Git commits or repetitive checkpoints solely for bookkeeping.";
}
