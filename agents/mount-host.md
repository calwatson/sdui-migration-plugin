---
name: mount-host
description: >-
  Wire SDUI into the existing app for one island: native chrome, pretty route,
  fetchScreen/validateScreen/SduiRenderer, navigate map, BFF rewrite or route
  if the flow writes. Does not add composers.
---

# mount-host

Follow `sdui-host-hybrid` and, if writes exist, `sdui-bff-io`.

1. Keep existing chrome in the host layout. Do not put the header inside the screen loader.
2. Add pretty route(s) for the agreed screen ids. Map `onNavigate` via a `pathForScreen` table. `home` may be `/` native.
3. Loader: `fetchScreen` → `validateScreen` → `SduiRenderer` with `onHttp: submitHttpAction` when the flow posts.
4. Point the screen origin env at layout-service, not the domain API.
5. If checkout/write: same-origin path in JSON; rewrite or route handler to the BFF/domain mapper. Do not POST to layout-service.

Do not compose screen trees here. Do not replace native account/home unless that is the island.
