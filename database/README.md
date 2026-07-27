# Database

MySQL 8 is the system of record. Phase 2 will add the normalized logical model, constraints, indexes, migration tooling, and deterministic seed data. Database changes must always be expressed as reversible migrations; application startup must never create or mutate production tables implicitly.

