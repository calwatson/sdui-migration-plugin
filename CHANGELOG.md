# Changelog

## 0.2.0

- Scute domain track: `scute-hexagon` (vendored kernel, ports, adapters, ProblemDetail mapping, ArchUnit gate) and `scute-migrate-domain` (per-island conversion sequence), with the `inventory-domain` and `hexagon-slice` subagents.
- `sdui-migrate-flow` gained a domain step between inventory and compose. It only runs on Java/Spring backends; every other stack keeps its existing APIs.
- Endpoint contracts are frozen across conversion — same paths, methods, field names — so composers and the BFF are untouched. `sdui-verify` now checks that, plus the ArchUnit gate, use-case tests, and error mapping.
- `sdui-plan-migration` and `map-domains` record backend stack per domain and whether the Scute track applies. Stack does not affect flow ranking.
- Hooks fire on hexagon Java files as well as composers, reminding about the ArchUnit gate and the contract freeze.
- `sdui-plan-migration` + `map-domains`: whole-app domain/flow ranking before compose. `sdui-migrate-flow` waits for a confirmed island.
- Fix hooks never loading: moved to `hooks/hooks.json` + `scripts/`, the plugin discovery path. A plugin-internal `.cursor/hooks.json` is not read.
- Document that registering the folder as a local plugin repo only offers the plugin; components load after **Install**. Registering it both as a marketplace and in `~/.cursor/plugins/local` conflicts.

## 0.1.0

- Initial plugin: seams rule, six skills, three subagent defs, fail-open composer hooks.
