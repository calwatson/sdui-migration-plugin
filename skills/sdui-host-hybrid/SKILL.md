---
name: sdui-host-hybrid
description: >-
  Mount SDUI inside an existing app: native chrome and pages, pretty routes for
  selected screens, pathForScreen navigate map, body-only host shell, fetchScreen
  and validateScreen. Use when editing a host, Next/SPA shell, hybrid routing,
  or wiring SduiRenderer.
disable-model-invocation: true
---

# Hybrid host

The existing app is the product. SDUI is an island.

## Native vs SDUI

- **Native:** layout chrome (nav, auth), marketing/home, account/settings unless those flows are the migration target.
- **SDUI:** only the agreed routes (example pattern: `/shop` → `catalog`, `/checkout` → `checkout`, `/orders` → `orders`).

Do not fetch a composed `home` screen just to render a landing page.

## Chrome

Header/nav lives in the **host layout**, not inside the screen loader. The loader is body-only: loading, error, invalid payload, `SduiRenderer`.

## Navigation

Map screen ids to **host** paths. Example:

```ts
const SCREEN_PATHS: Record<string, string> = {
  home: "/",
  catalog: "/shop",
  checkout: "/checkout",
  "order-placed": "/order-placed",
  orders: "/orders",
};

export function pathForScreen(screenId: string): string {
  return SCREEN_PATHS[screenId] ?? "/";
}
```

`onNavigate` → `router.push(pathForScreen(id))` (or the host’s equivalent). Avoid a catch-all `/s/:id` for the whole app.

## Load path

```ts
const fetched = await fetchScreen(screenId, process.env.NEXT_PUBLIC_SCREEN_SERVICE_ORIGIN);
if (!fetched.ok) { /* host error UI */ }
const result = validateScreen(fetched.payload, hostRegistry);
if (!result.success) { /* show result.errors; do not render */ }
// SduiRenderer: screen, registry, onNavigate, onNotify, onHttp: submitHttpAction
```

`NEXT_PUBLIC_SCREEN_SERVICE_ORIGIN` (or equivalent) is the layout-service origin. It is not the domain API.

## Stack note

Next.js App Router is the reference host. The same split applies to any SPA: layout chrome + route modules that only mount the loader. Do not require Next rewrites for reads.
