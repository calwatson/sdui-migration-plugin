---
name: sdui-layout-ports
description: >-
  layout-service composition: resolveScreen looks up a registry of TypeScript
  composers; domain access is ports plus an HTTP adapter, not a switch on
  screen ids. Use when adding screens, DomainSource/ports, composers, or
  GET /api/screens.
disable-model-invocation: true
---

# Layout-service ports and registry

## Kernel (do not fork)

```ts
type ScreenComposer = () => Promise<SduiScreen>;
type ScreenRegistry = ReadonlyMap<string, ScreenComposer>;

resolveScreen(id: string, registry: ScreenRegistry): Promise<ScreenResult>
```

- Invalid id charset → 400
- Missing key → 404
- Composer throws `DomainUnavailableError` → 502 (`The domain source did not return ${resource}.`)
- Else 200 with the tree

The kernel has no catalog/orders/customer types.

## Ports

One port per resource the composers need, e.g.:

```ts
type CatalogPort = { list: () => Promise<CatalogItem[]> };
type OrdersPort = { list: () => Promise<Order[]> };
type AppPorts = { catalog: CatalogPort; orders: OrdersPort };
```

HTTP adapter (customer origin, not hardcoded Scute) implements those ports. GET only.

## Registry

Close ports over composers:

```ts
export function appRegistry(ports: AppPorts): ScreenRegistry {
  return new Map([
    ["catalog", async () => catalog(await ports.catalog.list())],
    ["checkout", async () => checkout()],
  ]);
}
```

Server: `resolveScreen(id, appRegistry(customerPorts(origin)))`.

Adding a screen: new composer function + one map entry. New port only if a new resource. **Do not edit `resolve.ts`.**

Still one TypeScript composer per screen. No template/fetch-and-fill engine.
