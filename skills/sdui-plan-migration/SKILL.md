---
name: sdui-plan-migration
description: >-
  Identify domains and user flows inside an existing app and rank them for SDUI
  migration. Use when the user asks what to migrate, which screens or domains
  to convert, to plan an SDUI engagement, or to build a migration backlog
  before composing screens.
---

# Plan domains and flows

Read `sdui-architecture` first. This step is **read-only**. Do not add composers, host routes, or a BFF.

A **domain** is a bounded context around resources and APIs (catalog, orders, account). A **flow** is a user journey that will become one or more `screenId`s (browse → checkout → confirmation). Ports follow domains. Screen composers follow flows. Do not treat every route as a flow.

## Sequence

1. **Scan the app** — Launch `map-domains` (or do it yourself if the app is tiny). Cover routes/nav, feature folders, API clients, chrome vs page body, and which backend serves each domain. Do not stop at the first list page.
2. **Group** — Cluster routes and fetches into domains. Then name the flows that cross those surfaces. A flow that spans two domains is still one flow; it will need two ports, not two migrations.
3. **Score each flow** — Use the rubric below. Stay native is a valid outcome.
4. **Recommend** — Rank a backlog. Pick **one** first flow. Stop and confirm with the user before `sdui-migrate-flow` composes anything.

If the user already named a flow, still produce the domain map so ports land in the right bounded context. Skip ranking the rest unless they asked for a backlog.

## Fit rubric

Prefer as **first** SDUI island:

- Read-heavy list or list → detail
- Domain data already exposed as JSON GETs (or a thin adapter is obvious)
- Body widgets fit Stack, Row, Text, Heading, Image, Card, Button, Badge, Divider, Spacer, Input
- Writes are zero or one same-origin POST
- Journey is bounded (a few screens, not the whole shell)

Keep **native** (or defer):

- App chrome, auth, session, global nav
- Canvas, maps, drag-and-drop, heavy local state, realtime editors
- Screens that need many widgets not in the host registry
- Domain APIs that already return UI JSON (split domain vs composition first; do not wrap that payload as a screen)

A domain can be a good port owner even when none of its flows should migrate yet.

Backend stack does not change a flow's fit. Record whether the Scute track applies (see `scute-migrate-domain`) so the island's scope is honest, but do not rank a flow higher because its backend is Java.

## Output

```markdown
# SDUI migration plan

## Domains
| Domain | Resources / GETs | Used by flows | Backend stack | Scute track | Notes |
| --- | --- | --- | --- | --- | --- |

## Flows (ranked)
| Rank | Flow | Screen ids (proposed) | Domain ports | Writes (BFF?) | Fit | Why |
| --- | --- | --- | --- | --- | --- | --- |

Fit: `first` | `later` | `native`. Scute track: `yes` (Java/Spring, convertible) | `no` (other stack, third party, or already a hexagon).

## First island
- Flow:
- Why this one:
- Surfaces that stay native in the same routes (chrome, etc.):
- Registry gap for this flow:
- Domain slice: (base package and endpoints if the Scute track applies, else why not)

## Out of scope
- (chrome, auth, and any flow marked native, with one-line why)
```

Do not invent screen ids for surfaces you did not find. Do not propose rewriting the app or a template engine.

## After the user confirms

Hand the chosen flow to `sdui-migrate-flow`. That skill’s inventory step is a **deep dive** on the island (widget-level, BFF paths), not a second whole-app scan.
