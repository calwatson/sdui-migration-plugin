---
name: scute-hexagon
description: >-
  Target domain architecture for Java/Spring backends behind SDUI: vendored Scute
  kernel annotations, domain/application/adapter packages, inbound and outbound
  ports, ProblemDetail error mapping, ArchUnit gate. Use when discussing Scute,
  hexagonal or ports-and-adapters structure, @UseCase services, or converting a
  customer's Spring controllers into a hexagon.
disable-model-invocation: true
---

# Scute hexagon

## Target

One bounded context per base package. Nothing above the hexagon knows how it stores data; nothing inside it knows it is served over HTTP.

```
<base>/
  domain/                    entities, value objects, invariants — no framework imports
  application/
    port/in/                 @InboundPort interfaces (one per use case)
    port/out/                @OutboundPort interfaces (one per driven dependency)
    *Service.java            @UseCase implementations of port/in
  adapter/
    in/web/                  @RestController + request/response records
    out/<name>/              implementations of port/out
```

`layout-service` ports call `adapter/in/web` over GET. The host BFF calls it for writes. Neither reaches past the controller.

## Vendored kernel

Scute is not published. Copy the kernel into the customer repo under `<customerBase>.hexagon` instead of adding a dependency, keeping **type names identical** so a later swap to `io.scute:scute-kernel` is an import change:

| Type | Purpose |
| --- | --- |
| `UseCase` | marks an application service |
| `InboundPort` | driving contract, consumed by `adapter/in` |
| `OutboundPort` | driven contract, implemented by `adapter/out` |
| `DomainException` | base runtime exception |
| `NotFoundException`, `ConflictException`, `ValidationException` | subclasses the REST handler maps |

Vendored `@UseCase` is meta-annotated `@Component` + `@Transactional`:

```java
@Documented
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Component
@Transactional
public @interface UseCase {}
```

That is the one deliberate divergence from upstream Scute, where `@UseCase` is a bare marker picked up by `UseCaseScanningRegistrar` via `@HexagonApplication`. Component scanning already reaches the customer's packages, so do **not** vendor the registrar or swap their `@SpringBootApplication` annotation.

`@InboundPort` and `@OutboundPort` stay bare markers. They document the seam; ArchUnit enforces it.

## Ports and use cases

- One inbound port per use case, named for the action (`ListProducts`, `PlaceOrder`), with a single `execute`. Commands are nested records: `record Command(...) {}`.
- One `@UseCase` service per inbound port, constructor-injected with outbound ports only.
- Outbound ports are named for what the hexagon needs (`ProductRepository`, `ProductCatalog`), not for the technology behind them.
- Domain types carry the invariants. Validation that belongs to a value object (`new ProductName(...)` throwing `ValidationException`) does not belong in the controller.

## Adapters

Inbound: `@RestController` translates transport to port calls and domain objects to response records. It holds no business rules and never touches `adapter/out`.

Outbound in a **thin hexagon**: the adapter delegates to the service or repository the customer already has. It is the only place legacy types are allowed, and it converts them to domain types at the boundary.

```java
@Component
class LegacyProductRepositoryAdapter implements ProductRepository {

    private final LegacyCatalogService legacy;

    LegacyProductRepositoryAdapter(LegacyCatalogService legacy) {
        this.legacy = legacy;
    }

    @Override
    public List<Product> findAll() {
        return legacy.loadCatalog().stream().map(ProductMapper::toDomain).toList();
    }
}
```

Do not move persistence, rewrite JPA entities, or delete the legacy service as part of the first island. `@PersistenceAdapter` and `scute-adapter-jpa` are for later, once a slice actually owns its storage.

## Errors

Vendor `HexagonRestExceptionHandler` as a `@RestControllerAdvice` in the customer's web adapter package:

| Exception | Status |
| --- | --- |
| `NotFoundException` | 404 |
| `ConflictException` | 409 |
| `ValidationException`, `MethodArgumentNotValidException` | 400 |
| `DomainException` | 400 |

Responses are RFC 7807 `ProblemDetail`. That is the shape `sdui-bff-io` already reads `detail` from to build `{ error }`, so do not invent a second error envelope.

## Architecture gate

Copy `HexagonArchitecture` into test sources and scope it to the converted package only:

```java
@AnalyzeClasses(packages = "com.acme.catalog", importOptions = ImportOption.DoNotIncludeTests.class)
class CatalogHexagonArchitectureTest {

    @ArchTest
    static final ArchRule hexagon = HexagonArchitecture.rules("com.acme.catalog");
}
```

Needs `com.tngtech.archunit:archunit-junit5` in the test configuration. The rules:

- Layering: `domain` may be used by `application` and `adapter`; `application` only by `adapter`; nothing may use `adapter`.
- `domain` and `application` may not depend on `org.springframework..`, `jakarta.persistence..`, `jakarta.servlet..`, `org.hibernate..`.
- `adapter.in` and `adapter.out` may not depend on each other.

Never point the gate at a legacy root package to "see how bad it is". A red suite on unconverted code trains everyone to ignore it.

## Hard seams

- The hexagon does not emit UI JSON. Screen trees are `layout-service`'s job.
- Endpoint paths do not change during conversion. Composers and the BFF must keep working untouched.
- No Spring or JPA types inside `domain` or `application`, including in method signatures.
- `adapter/out` converts legacy or persistence types to domain types. Legacy types must not surface in a port signature.
- One island's slice is one bounded context. Two flows sharing a domain share the package; they do not get two hexagons.
