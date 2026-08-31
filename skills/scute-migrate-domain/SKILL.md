---
name: scute-migrate-domain
description: >-
  Convert the Java/Spring backend slice behind one SDUI island into a thin Scute
  hexagon: vendor the kernel, carve domain and ports, delegate to existing
  services, gate with ArchUnit. Use when migrating a flow's domain to Scute,
  adding a hexagon to a customer backend, or asked to convert controllers and
  services to ports and adapters.
---

# Migrate one domain slice to Scute

Read `scute-hexagon` first. This runs **inside** `sdui-migrate-flow`, after the island is confirmed and inventoried, before composers are written against the endpoints.

Convert the slice that the confirmed island reads and writes. Nothing else.

## Applies when

- The backend behind the island is **Java + Spring Boot** (Gradle or Maven).
- The endpoints the flow needs are owned by that codebase, not a third party.

Otherwise skip this track entirely and keep their existing APIs as the domain. The SDUI half does not depend on the backend being a hexagon.

## Sequence

1. **Detect** — find the Spring Boot app for those endpoints: build file (`build.gradle(.kts)` or `pom.xml`), Java toolchain version, `@SpringBootApplication` class and its package, test framework. Record the build tool; every dependency edit below goes in that file.
2. **Inventory** — launch `inventory-domain` (or do it yourself if the slice is two endpoints). It reports the controllers, services, and repositories behind each GET the composers need and the one POST the BFF calls, plus a proposed base package and port set.
3. **Vendor the kernel** — once per repo, not once per slice. Copy the seven kernel types into `<customerBase>.hexagon` and `HexagonArchitecture` into test sources; add `com.tngtech.archunit:archunit-junit5` to the test configuration. If `<customerBase>.hexagon` already exists, reuse it.
4. **Carve the slice** — launch `hexagon-slice` per bounded context (usually one). Domain types, `port/in`, `port/out`, `@UseCase` services, `adapter/in/web`, delegating `adapter/out`.
5. **Keep the contract** — the new controller answers the **same paths, methods, and JSON field names** as the old one. Diff a response body before and after; composers and the BFF must not need an edit.
6. **Retire the old entry point** — once the new controller serves the path, delete the old controller method it replaced. Leave the legacy service in place; `adapter/out` calls it.
7. **Gate** — add the `HexagonArchitecture` test scoped to the new base package. Add use-case tests against in-memory outbound fakes.
8. **Verify** — follow `sdui-verify`. Domain gates and SDUI gates both run before the island is done.

## Thin, on purpose

The first slice moves **structure**, not storage:

- Outbound adapters delegate to existing services and repositories.
- No JPA entity rewrite, no schema change, no `@PersistenceAdapter`, no new datasource.
- Business rules move into `domain` and `@UseCase` only where they already live in the code you are wrapping. Do not invent invariants nobody asked for.

A slice that "needed" a persistence rewrite to compile was scoped too wide. Narrow it.

## Stop conditions

- **Not Java/Spring** — skip the track, say so, continue with SDUI against the existing APIs.
- **Controllers already return UI JSON** — split domain from composition first; do not wrap a screen payload in a port.
- **The slice pulls in unrelated packages** — if the ports cannot be satisfied without touching contexts outside the island, stop and report the boundary you hit. Do not expand the island to make the hexagon tidy.
- **No test setup at all** — the ArchUnit gate and use-case tests are the deliverable, not an extra. Get a test task running first, or stop and say so.
- **Endpoints are shared with other consumers** (mobile app, partner API) — the contract freeze in step 5 is now load-bearing. Confirm before touching those controllers.

## Output

Report: base package chosen, ports added, which legacy services the outbound adapters delegate to, endpoints that changed hands (path by path, with "contract unchanged" stated explicitly), and what stayed legacy.
