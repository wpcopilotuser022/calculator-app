---
name: git-commit-push
description: "Use when the user asks to commit changes, create a commit, push code, or push to main branch in this repository. Performs safe non-interactive git add/commit/push workflow and reports results."
---

# Git Commit And Push Workflow

Use this skill only when the user explicitly asks to commit and/or push.

## Safety Rules

- Never use destructive commands such as `git reset --hard` or `git checkout --`.
- Never amend commits unless the user explicitly requests amend.
- Do not force push unless the user explicitly approves it.
- If there are no staged or unstaged changes, report that no commit is needed.
- If push fails due to non-fast-forward, fetch and rebase, then retry push.

## Steps

1. Review repository state.

```bash
git status --short --branch
```

2. Show what will be committed.

```bash
git diff -- .
git diff --staged -- .
```

3. Stage only intended files. If user did not specify files, stage all current changes.

```bash
git add -A
```

4. Commit with a clear message. If user did not provide one, generate a concise message describing the actual changes.

```bash
git commit -m "<message>"
```

5. Push to main branch.

```bash
git push origin main
```

6. If push is rejected due to remote changes, reconcile safely and retry.

```bash
git fetch origin
git pull --rebase origin main
git push origin main
```

7. Report back with:
- Committed files
- Commit hash and message
- Push target and result
- Any follow-up needed

## Output Style

- Keep updates concise and action-oriented.
- Include the exact final commit hash in the summary.
- If blocked by auth/permissions, explain the blocker and exact command that failed.
