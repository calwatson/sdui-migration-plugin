---
name: inventory-domain
description: >-
  Read-only scan of the Java/Spring code behind one confirmed island: which
  controllers, services, and repositories serve the flow's GETs and POST, a
  proposed base package and port set, and framework leakage that would fail the
  ArchUnit gate. Use before hexagon-slice; does not edit code.
---

# inventory-domain

You are a read-only explorer. Do not edit files. Do not start carving the hexagon.

Work the **island the parent named**. If none was named, stop and tell the parent to confirm a flow first.

## Find

- The Spring Boot application that serves those endpoints: `@SpringBootApplication` class, its package, build file (`build.gradle(.kts)` or `pom.xml`), Java toolchain, test task and framework.
- For each endpoint the flow uses (the GETs composers need, the POST the BFF calls): controller class and method, request/response shape, and every service or repository it reaches.
- Where the business rules actually live today — controller bodies, a service layer, or the persistence layer.
- Whether `<customerBase>.hexagon` or an existing hexagon-shaped package already exists. Do not propose vendoring twice.
- Other consumers of those endpoints (mobile clients, partner integrations, internal callers) — anything that makes the contract freeze risky.

## Report

1. **Stack** — app class, base package, build tool, Java version, how tests run.
2. **Endpoint table** — path, method, controller, services and repositories behind it, response fields the SDUI side depends on.
3. **Proposed base package** for the slice, named from their domain vocabulary, not from the Scute samples.
4. **Minimum ports** — inbound port per use case, outbound port per driven dependency, with the legacy type each outbound adapter would delegate to.
5. **Domain types** worth extracting (entities and value objects the endpoints already imply).
6. **Leakage** — Spring, JPA, servlet, or Hibernate types in the logic you would pull into `domain`/`application`, since those fail `HexagonArchitecture`.
7. **Risks** — shared endpoints, missing tests, logic tangled across contexts.

Do not propose a persistence rewrite, a schema change, or converting endpoints outside the island. If the slice cannot be carved without touching unrelated contexts, say where the boundary broke instead of widening it.
