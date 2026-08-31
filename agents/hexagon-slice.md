---
name: hexagon-slice
description: >-
  Carve one bounded context into a thin Scute hexagon: domain types, inbound and
  outbound ports, @UseCase services, web adapter, delegating outbound adapter,
  ArchUnit and use-case tests. Keeps endpoint contracts identical; does not touch
  persistence or SDUI composers.
---

# hexagon-slice

Implement **one** bounded context. Follow `scute-hexagon`. Read `scute-migrate-domain` if the scope is unclear.

1. Vendor the kernel into `<customerBase>.hexagon` if it is not there yet: `UseCase`, `InboundPort`, `OutboundPort`, `DomainException`, `NotFoundException`, `ConflictException`, `ValidationException`, plus `HexagonArchitecture` in test sources and the `archunit-junit5` test dependency. Reuse it if it exists.
2. `domain/` — entities and value objects with their invariants. No framework imports, including in signatures.
3. `application/port/in/` — one `@InboundPort` per use case with a single `execute`; nested `record Command(...)` for multi-field input.
4. `application/port/out/` — one `@OutboundPort` per driven dependency, in the hexagon's vocabulary.
5. `application/` — a `@UseCase` service per inbound port, constructor-injected with outbound ports only.
6. `adapter/in/web/` — `@RestController` on the **same paths, methods, and JSON field names** as the endpoint it replaces, with request/response records. Add the vendored `HexagonRestExceptionHandler` advice if the repo has no equivalent.
7. `adapter/out/` — implement each outbound port by delegating to the existing service or repository, mapping legacy types to domain types at the boundary. No JPA entity work.
8. Delete the old controller method the new one replaces. Leave the legacy service alone.
9. Tests — `HexagonArchitecture.rules("<base>")` scoped to the new package only, plus use-case tests driven through in-memory outbound fakes.

Stay inside the slice. Do not change endpoint paths or response fields, rewrite persistence, touch SDUI composers or the host, or point the ArchUnit gate at legacy packages.
