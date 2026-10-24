# Claude Code config

The global Claude Code config. `claude/install.sh` links it into `~/.claude`.
It was in the dotfiles repo before, as a package that stow did not manage.

## Why not stow

`~/.claude` mixes user config with Claude's runtime state (`history.jsonl`,
`sessions/`, `cache/`, `projects/`, `todos/`, ...) that must never be in git, so
the whole directory can't be symlinked. Worse, Claude rewrites `settings.json`
at runtime (toggling `/config` options), which replaces a stow symlink with a
plain file — silently breaking the link and dirtying the repo with
machine-specific values (absolute paths, model choice, plugin toggles).

## How it works

Run `bash claude/install.sh` (dotfiles' freyr does this automatically; `--force` re-seeds
the settings baseline). It is idempotent.

- **Symlinked** (repo is the source of truth, edits are live everywhere):
  `hooks/`, `output-styles/`, `agents/`, `commands/`,
  `statusline-command.sh`, `CLAUDE.md`. Symlinks are per-item, so machine-only entries
  are preserved.
- **Copied baseline** — `settings.json`: portable defaults, seeded only when
  missing. Claude owns it at runtime; it is never symlinked or overwritten
  (use `--force` to re-seed from the baseline, which backs up the existing one).
- **Never touched** — `settings.local.json`: per-machine permission allowlists.
  Gitignored.

## Skills

The installer does not link skills. A global skill is in the context of every session,
so keep that list short. Copy a skill into one project with `agentkit add NAME`. Link a
skill for every session with `agentkit add --global NAME` (now: `blind-spots`).

## Machine-local / private content

`settings.local.json` and `agents/` are gitignored (see repo `.gitignore`).
The agents currently reference internal project names, so they stay local to
each machine — the installer symlinks them if present but they are never
committed to this public repo. They are not backed up anywhere except locally.
