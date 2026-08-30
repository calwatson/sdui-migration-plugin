---
name: sdui-verify
description: >-
  Quality gates for SDUI work: composed trees validate against the host registry,
  kernel 400/404/502, native pages do not fetch screens, BFF mapping tests. Use
  before finishing composers, host mounts, or BFF changes.
disable-model-invocation: true
---

# SDUI verify

Before calling the work done:

1. **Contract** — every composed screen in the registry: `validateScreen(body, hostRegistry)` succeeds (empty extra-prop / unknown-type errors).
2. **Kernel** — invalid id 400, unknown id 404, `DomainUnavailableError` 502. Use a fake registry; do not require the customer’s live API.
3. **Adapter** — port HTTP wrapper: transport failure and non-OK status become `DomainUnavailableError`.
4. **Native pages** — home/account (or equivalent) do not call `fetchScreen`.
5. **Host loader** — mocked fetch still hits `{layoutOrigin}/api/screens/{id}`.
6. **BFF** — extra local-state keys are not forwarded; `{ error }` comes from `detail` when present.

Run the layout-service (or customer equivalent) test suite and the host suite that covers the new route.

If browser tools exist and the host UI changed, exercise the flow: native chrome persists on the SDUI route; one static and one data-backed screen render. If not, say what was not clicked.
