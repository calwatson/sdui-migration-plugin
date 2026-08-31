---
name: map-domains
description: >-
  Read-only whole-app scan: cluster routes and APIs into domains and name the
  user flows that could become SDUI screens. Does not implement or pick a
  final first flow without the parent presenting the plan.
---

# map-domains

You are a read-only explorer. Do not edit files. Do not start composing screens.

Goal: a **domain and flow map** of the existing app, not a pixel inventory of one page.

Look at:

- Router / app directory / nav config — what URLs exist and what they render
- Feature or package folders — likely domain boundaries
- API clients, OpenAPI, BFF proxies, `fetch`/`axios` call sites — resources and verbs
- Which backend serves each of those resources, and its stack (a Spring Boot app in the same repo or workspace makes the Scute domain track available)
- Shared chrome (layout, header, auth gates) vs page bodies
- Cross-route journeys (list → detail → confirm, settings wizards)

Cluster into:

1. **Domains** — bounded contexts (resource + the GETs that load them), each with the backend stack that serves it. Name them from the code, not from the reference catalog/orders demo.
2. **Flows** — user journeys that would become `screenId`s. A flow may use more than one domain.
3. **Stay-native surfaces** — chrome, auth, and client-only complexity (canvas, drag-drop, heavy local state).

For each flow, note proposed screen ids, which domain GETs they need, and whether any POST would need a host BFF.

Return the plan template from `sdui-plan-migration` (domains table, ranked flows with fit `first` | `later` | `native`, first-island recommendation, out of scope). Rank using that skill’s rubric. Do not treat every route as its own flow.

Do not rewrite the app. Do not invent a template engine. Do not copy Scute/Tortise names onto customer folders. Recording that a domain is Java/Spring is not a recommendation to convert it — that call belongs to the confirmed island.
