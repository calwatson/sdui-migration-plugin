---
name: sdui-architecture
description: >-
  Target SDUI architecture for migrating existing apps: hybrid host, layout-service
  composers on a registry with domain ports, shell BFF for writes, sdui-core
  fetch/validate/render. Use when discussing SDUI, screen composition, layout-service,
  server-driven UI, or migrating a customer app onto JSON screens.
disable-model-invocation: true
---

# SDUI architecture

## Target

The customer keeps **their app as the shell** and **their APIs as domain**. Selected flows become versioned screen JSON.

```
Existing app (chrome, auth, native routes)
  -> sdui-core (fetchScreen, validateScreen, SduiRenderer)
       -> layout-service GET /api/screens/:id (composers + registry + ports)
            -> customer domain GET APIs

Existing app same-origin POST /api/... (http actions)
  -> host BFF
       -> customer domain writes
```

## Seams

- Domain does not emit UI trees.
- layout-service **reads** domain data to compose. It never handles writes.
- Hosts **fetch, validate, render**. Unrelated pages stay native React/HTML/whatever they already have.
- `http` actions in JSON are **same-origin paths**. The shell (or its BFF) maps them onto domain commands.
- `schemaVersion: 1` trees: `{ schemaVersion, screenId, title?, root }`. Nodes: `{ id, type, props?, children?, actions? }`.
- Strict component registry: unknown `type` or extra props fail validation. Do not invent primitives for one screen unless the host registry is explicitly extended.

## What not to copy from the reference stack

- Scute is one hexagon demo, not the customer’s domain.
- Tortise is a **reference hybrid host**, not a product to deploy.
- Studio is an inspector, not the customer shell.
- Do not require Next.js. Pretty routes + chrome-in-layout is the pattern; Next rewrites are **one** BFF implementation.

## One flow first

Migrate a bounded flow (list → detail/checkout → confirmation). Leave dense client-only UI native until the registry and action model can carry it.

If the island is not chosen yet, follow `sdui-plan-migration`: domains own ports, flows own screen ids. Do not start from a route dump.
