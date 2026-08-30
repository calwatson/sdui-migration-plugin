---
name: sdui-bff-io
description: >-
  Shell-owned writes for SDUI: host-relative http actions, BFF maps local state
  onto a domain command, RFC 7807 becomes { error } for submitHttpAction. Use
  when implementing checkout, POST actions, BFF gateway, or order placement.
disable-model-invocation: true
---

# Shell BFF I/O

layout-service never accepts writes. Screen JSON uses same-origin paths:

```ts
onPress: {
  type: "http",
  method: "POST",
  path: "/api/orders", // host origin, not https://domain.example
  bodyFromState: true,
  onSuccess: { type: "navigate", screenId: "order-placed" },
}
```

`submitHttpAction` POSTs that path with the **entire** local state blob. The BFF must pick the fields the domain command needs and drop the rest.

## BFF responsibilities

- Validate email/sku/qty (or the customer’s command shape) before calling domain
- Map string quantities from inputs to the domain type
- Translate ProblemDetail/`detail` into `{ error: string }` so the renderer can toast
- 502 if the domain API is unreachable
- Optional GET proxy for the same resource if the host already rewrote those paths

## Host wiring

The browser must not call the domain API directly. Options:

- Next (or other) **rewrite** `/api/orders` → BFF origin
- Host **route handler** that *is* the BFF
- Existing customer BFF: keep its public path; put that path in the screen JSON

Next rewrite is one shape. Prefer the customer’s existing BFF if they have one.

## Contract

`sdui-core` only allows `http` method POST and paths starting with `/`. Do not put absolute domain URLs in screen actions.
