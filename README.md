# sdui-migration-plugin

Cursor plugin for migrating **existing apps** onto a server-driven UI split: the customer app stays the shell; layout-service composes screen JSON; writes go through a host BFF.

Scute, Tortise, and SDUI Studio are a **reference implementation**, not what the customer deploys. This plugin must work in their repo without those folders.

## Ultimate goal

Keep their chrome, auth, and APIs. Convert **one flow** at a time onto versioned screen trees that hosts validate before render.

## Components

### Rule

- `rules/sdui-seams.mdc` (always applied) — hard seams; load `sdui-architecture` before coding SDUI work.

### Skills

| Skill | Use when |
| --- | --- |
| `sdui-architecture` | Any SDUI / composition / migration discussion |
| `sdui-plan-migration` | Identify domains and rank flows before composing |
| `sdui-migrate-flow` | User asks to migrate an app or a flow (orchestrator) |
| `sdui-host-hybrid` | Host routing, chrome, mounting `SduiRenderer` |
| `sdui-layout-ports` | Composers, registry, domain ports |
| `sdui-bff-io` | Same-origin writes, BFF mapping |
| `sdui-verify` | Before finishing: contract tests and gates |

### Agents

Used from the planner and orchestrator via Task: `map-domains`, `inventory-ui`, `compose-screen`, `mount-host`.

### Hooks

Plugin hooks live in `hooks/hooks.json` with their scripts in `scripts/` — that is the path plugin installation reads. A plugin-root `hooks.json`, or a `.cursor/hooks.json` inside the plugin, is **not** loaded.

- `afterFileEdit` — if a composer/registry file was edited, remind the agent to validate trees
- `stop` — if those files were in play, remind `sdui-verify`

Both fail open: bad JSON or a crash prints `{}` and never blocks the user. Matching is path-based, so prose that merely mentions a composer does not trigger them.

```bash
python3 scripts/test_hooks.py
```

## Installation

This repo is shaped as a **single-plugin marketplace**: `.cursor-plugin/marketplace.json` is the catalog and `.cursor-plugin/plugin.json` is the plugin, with `"source": "."`.

### As a local plugin repo (marketplace)

Register this folder in **Customize** as a local plugin repo, then **Install** `sdui-migration-plugin` from the catalog. Reload the window if components do not appear.

Registering is not installing. The catalog only makes the plugin *offerable*; until you click Install, no skills, rules, or agents load. A successful parse looks like this in the logs, and by itself means nothing is active yet:

```
[PluginsProviderService] Persisted locally parsed marketplace:
sdui-migration-marketplace with 1 plugin(s)
```

Install resolves a **git revision**, so the folder must be a git repo with at least one commit. Uncommitted edits are invisible to the installed copy: commit, then refresh the marketplace and reinstall to pick up changes.

Keep `version` identical in both manifests. Cursor serves the catalog's version, so bumping only `plugin.json` ships a stale entry.

### Alternative: load directly, no install click

Drop the plugin in `~/.cursor/plugins/local` instead and Cursor loads it on reload. This path wants a plugin, **not** a catalog — with `marketplace.json` present, the folder is indexed as a marketplace and nothing loads. Move that file out first:

```bash
mkdir -p ~/.cursor/plugins/local
ln -sfn "$PWD" ~/.cursor/plugins/local/sdui-migration-plugin
```

Pick one mechanism. Registering the same folder both ways gives Cursor two conflicting readings of it.

If nothing appears either way, local plugins may be disabled for your org: **Allow Local Plugin Imports** under Dashboard → Settings → Security & Identity → Marketplace and Plugins (off by default on Enterprise). A marketplace plugin with the same name also takes precedence over a local copy.

### Sharing with teammates

```bash
git init && git add . && git commit -m "Initial plugin"
git remote add origin <remote-url> && git push -u origin HEAD
```

Teammates add the remote as a marketplace in Customize (or Dashboard → Plugins → Add Marketplace) and install from there.

### Customer repo without plugins

Copy into the customer project:

- `rules/` → `.cursor/rules/`
- `skills/` → `.cursor/skills/`
- `agents/` → `.cursor/agents/`
- `scripts/*.py` → `.cursor/hooks/`

Project hooks use a different file and path base than plugin hooks, so write `.cursor/hooks.json` in their repo:

```json
{
  "version": 1,
  "hooks": {
    "afterFileEdit": [{ "command": ".cursor/hooks/after-composer-edit.py" }],
    "stop": [{ "command": ".cursor/hooks/stop-verify.py", "loop_limit": 1 }]
  }
}
```

Keep `_sdui_paths.py` next to the two hook scripts; they import it by directory. Scripts must stay executable (`chmod +x .cursor/hooks/*.py`) and require `python3` on `$PATH`. Project hooks only run in a trusted workspace.

## License

MIT
