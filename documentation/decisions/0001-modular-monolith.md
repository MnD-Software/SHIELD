# ADR 0001: Start with a modular monolith

- Status: Accepted
- Date: 2026-07-21

## Context

Shield Pharmacy requires transactional consistency across catalog, stock, coupons, orders, and payments while initially operating as one product team.

## Decision

Use a Flask modular monolith with explicit domain services and provider adapters. Deploy one API service and one MySQL database, while maintaining module boundaries that can later become independently deployed services when measured scaling or ownership needs justify it.

## Consequences

Order placement and stock reservation can share reliable database transactions. Operations remain straightforward. Module contracts must be enforced through code review and tests so the codebase does not degrade into an unstructured monolith.

