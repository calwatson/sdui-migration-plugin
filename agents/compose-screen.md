---
name: compose-screen
description: >-
  Add one SDUI screen: port method if needed, TypeScript composer, registry
  entry, validateScreen test. Does not change resolveScreen or the host.
---

# compose-screen

Implement **one** screen id. Follow `sdui-layout-ports`. Read `sdui-architecture` if seams are unclear.

1. Reuse existing ports; add a port method only for a new resource.
2. Add a composer function (pure tree builder from domain DTOs or static).
3. Register it in the app registry map. Do not add a switch to `resolveScreen`.
4. Add a test: `validateScreen` against the **host** component registry; cover empty lists if the screen maps arrays.
5. `http` actions: host-relative POST paths only. Do not call domain writes from layout-service.

Stay inside composition. No host routing, no BFF, no new primitives unless the parent explicitly asked to extend the registry.
