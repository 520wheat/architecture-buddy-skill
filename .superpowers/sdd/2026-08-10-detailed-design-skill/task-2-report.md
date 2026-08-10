Status: done

Commits:
- 6ae95ef feat(skill): 增加详细设计 Skill 契约
- [pending] fix: clarify handoff path resolution and README flow

Test summary:
- Passed the brief’s package-contract checks (`test -f`, `rg`, and required-file non-empty validation).
- Round 1 verification passed after fixes: `rg` confirmed message-based path resolution, concrete direct/handoff sequences, explicit output layout, and “never code” wording.

Concerns:
- None.

Fix details:
- Clarified message-based relative path resolution to use the active repository/worktree root containing both the target Skill package and the architecture input, and require user selection when multiple roots are possible.
- Expanded README into concrete direct-invocation and architecture-handoff sequences, named the output layout, and stated the package produces documents only and never code.

Report path:
- /Users/apple/Desktop/skill-create/.worktrees/detailed-design-skill/.superpowers/sdd/2026-08-10-detailed-design-skill/task-2-report.md
