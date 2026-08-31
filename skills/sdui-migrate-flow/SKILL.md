---
name: sdui-migrate-flow
description: >-
  Orchestrates migrating one existing-app flow onto SDUI: plan domains if needed,
  inventory the island, add ports and composers, mount a hybrid host route, wire
  BFF writes, verify. Use when the user asks to migrate an app or screen flow,
  convert an existing UI to server-driven screens, or start an SDUI customer
  engagement.
---

# Migrate one flow

Read `sdui-architecture` first. Do not rewrite the whole app.

If the user has not named a flow (or asked what to migrate), follow `sdui-plan-migration` first. Stop after the plan until they confirm the island. Do not compose from an unconfirmed backlog.

## Sequence

1. **Plan** — Skip if a flow is already chosen. Otherwise follow `sdui-plan-migration` / `map-domains`: whole-app domains and ranked flows. Wait for confirmation.
2. **Inventory** — Launch the `inventory-ui` subagent (or do it yourself if the surface is tiny). Deep dive on the **chosen** flow only: chrome vs body, APIs, design-system components, registry gap. This is not a second app-wide scan.
3. **Domain (Java/Spring only)** — If the backend behind this island is Spring Boot and the engagement includes converting it, follow `scute-migrate-domain` (it may launch `inventory-domain`, `hexagon-slice`) before composers are written against those endpoints. Thin hexagon, one slice, unchanged paths. Any other stack: skip this step and keep their APIs as the domain.
4. **Compose** — For each screen id in that flow, launch `compose-screen` (or follow `sdui-layout-ports`). Ports per bounded context; one TypeScript composer per screen; register in the map. Kernel `resolveScreen(id, registry)` does not grow a switch.
5. **Mount host** — Launch `mount-host` (or follow `sdui-host-hybrid`). Chrome stays native. Pretty routes, not a catch-all `/s/:id` for the whole app. `fetchScreen` + `validateScreen` + `SduiRenderer`. Map `navigate` screen ids onto host paths.
6. **Writes** — If the flow POSTs, follow `sdui-bff-io`. Screen JSON keeps host-relative paths. BFF maps local state onto the domain command.
7. **Verify** — Follow `sdui-verify` before declaring done. If step 3 ran, its hexagon gates run too.

## Subagents

Use Task with these agent files’ instructions. They must not redesign seams.

- `map-domains` — whole-app plan (read-only)
- `inventory-ui` — chosen-flow deep dive (read-only)
- `inventory-domain` — backend behind the island (read-only, Java/Spring)
- `hexagon-slice` — one bounded context converted to Scute
- `compose-screen` — one screen id
- `mount-host` — host wiring for the island

## Stop conditions

- Customer APIs already return UI JSON — stop and split domain vs composition first. Do not "fix" it by wrapping the payload in a port either.
- Domain conversion would change an endpoint path or response field — stop. The island's composers and BFF depend on that contract.
- Flow needs widgets not in the host registry — either keep that surface native or extend the registry on purpose (see architecture). Do not smuggle extra props past validation.
