# Changelog

## Unreleased

- `sdui-plan-migration` + `map-domains`: whole-app domain/flow ranking before compose. `sdui-migrate-flow` waits for a confirmed island.
- Fix hooks never loading: moved to `hooks/hooks.json` + `scripts/`, the plugin discovery path. A plugin-internal `.cursor/hooks.json` is not read.
- Document that registering the folder as a local plugin repo only offers the plugin; components load after **Install**. Registering it both as a marketplace and in `~/.cursor/plugins/local` conflicts.

## 0.1.0

- Initial plugin: seams rule, six skills, three subagent defs, fail-open composer hooks.
