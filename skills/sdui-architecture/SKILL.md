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

The customer keeps **their app as the shell** and **their APIs as domain**. Selected flows become versioned screen JSON. Converting a domain to a Scute hexagon restructures what sits behind those APIs; it does not move the seam.

```
Existing app (chrome, auth, native routes)
  -> sdui-core (fetchScreen, validateScreen, SduiRenderer)
       -> layout-service GET /api/screens/:id (composers + registry + ports)
            -> customer domain GET APIs

Existing app same-origin POST /api/... (http actions)
  -> host BFF
       -> customer domain writes
```

The domain end of both arrows is the customer's existing API. On a **Java/Spring** backend, the slice behind a migrated island also becomes a hexagon, at the same URLs:

```
customer domain API (unchanged paths)
  -> adapter/in/web        REST controllers
       -> application      @UseCase services behind port/in
            -> domain      entities and value objects
       -> port/out         implemented by adapter/out (delegates to existing services)
```

See `scute-hexagon` for that half. It is optional: the SDUI seams hold whether or not the backend is converted.

## Seams

- Domain does not emit UI trees.
- layout-service **reads** domain data to compose. It never handles writes.
- Hosts **fetch, validate, render**. Unrelated pages stay native React/HTML/whatever they already have.
- `http` actions in JSON are **same-origin paths**. The shell (or its BFF) maps them onto domain commands.
- `schemaVersion: 1` trees: `{ schemaVersion, screenId, title?, root }`. Nodes: `{ id, type, props?, children?, actions? }`.
- Strict component registry: unknown `type` or extra props fail validation. Do not invent primitives for one screen unless the host registry is explicitly extended.
- Domain conversion keeps its HTTP contract: same paths, methods, field names. Composers and the BFF must not need an edit because a hexagon appeared.

## What not to copy from the reference stack

- Scute is a **domain architecture** the customer can adopt, not a service to deploy. Vendor the kernel into their packages; the sample catalog/orders names are not their domain.
- Tortise is a **reference hybrid host**, not a product to deploy.
- Studio is an inspector, not the customer shell.
- Do not require Next.js. Pretty routes + chrome-in-layout is the pattern; Next rewrites are **one** BFF implementation.

## One flow first

Migrate a bounded flow (list → detail/checkout → confirmation). Leave dense client-only UI native until the registry and action model can carry it.

If the island is not chosen yet, follow `sdui-plan-migration`: domains own ports, flows own screen ids. Do not start from a route dump.
